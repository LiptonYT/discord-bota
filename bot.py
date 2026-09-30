import os
import sqlite3
from datetime import datetime, timezone

import discord
from discord.ext import commands
from discord import app_commands


# =========================================================
# НАСТРОЙКИ
# =========================================================

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError("Не найден DISCORD_TOKEN")

GUILD_ID = 1533075462383730838

# Канал, где находится панель "Подать на повышение"
PROMOTION_PANEL_CHANNEL_ID = 1533076147204653159

# Канал, куда приходят заявки
PROMOTION_APPROVAL_CHANNEL_ID = 1554879440230817842

# Роль старшего состава
SENIOR_ROLE_ID = 1533075692785504327

DATABASE_FILE = "promotions.db"


# =========================================================
# ЗВАНИЯ
# =========================================================

RANK_NAMES = [
    "Рядовой",
    "Младший сержант",
    "Сержант",
    "Старший сержант",
    "Старшина",
    "Прапорщик",
    "Старший прапорщик",
    "Младший лейтенант",
    "Лейтенант",
    "Старший лейтенант",
    "Капитан",
    "Майор",
    "Подполковник",
    "Полковник",
    "Генерал-майор",
    "Генерал-лейтенант",
    "Генерал-полковник",
    "Генерал Российской Федерации",
]


# =========================================================
# DISCORD
# =========================================================

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


# =========================================================
# DATABASE
# =========================================================

def get_db():
    return sqlite3.connect(DATABASE_FILE)


def init_database():
    db = get_db()

    db.execute("""
        CREATE TABLE IF NOT EXISTS promotion_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            guild_id INTEGER NOT NULL,

            employee_id INTEGER NOT NULL,
            employee_name TEXT NOT NULL,

            submitted_by INTEGER NOT NULL,
            submitted_by_name TEXT NOT NULL,

            certificate_number TEXT NOT NULL,
            new_rank TEXT NOT NULL,
            reason TEXT NOT NULL,

            status TEXT NOT NULL DEFAULT 'pending',

            created_at TEXT NOT NULL,

            reviewed_at TEXT,
            reviewed_by INTEGER,
            reviewed_by_name TEXT,

            review_channel_id INTEGER,
            review_message_id INTEGER
        )
    """)

    db.commit()
    db.close()


def get_request(request_id):
    db = get_db()

    cursor = db.execute("""
        SELECT
            id,
            guild_id,
            employee_id,
            employee_name,
            submitted_by,
            submitted_by_name,
            certificate_number,
            new_rank,
            reason,
            status,
            created_at,
            reviewed_at,
            reviewed_by,
            reviewed_by_name,
            review_channel_id,
            review_message_id
        FROM promotion_requests
        WHERE id = ?
    """, (request_id,))

    row = cursor.fetchone()
    db.close()

    return row


def current_time():
    return datetime.now(timezone.utc)


# =========================================================
# ПРОВЕРКА СТАРШЕГО СОСТАВА
# =========================================================

def is_senior(member: discord.Member) -> bool:

    if member.guild_permissions.administrator:
        return True

    return any(
        role.id == SENIOR_ROLE_ID
        for role in member.roles
    )


# =========================================================
# ВЫБОР СОТРУДНИКА
# =========================================================

class EmployeeSelect(discord.ui.UserSelect):

    def __init__(self):
        super().__init__(
            placeholder="👤 Выберите сотрудника",
            min_values=1,
            max_values=1
        )

    async def callback(self, interaction: discord.Interaction):

        user = self.values[0]

        if user.bot:
            await interaction.response.send_message(
                "❌ Нельзя выбрать бота.",
                ephemeral=True
            )
            return

        self.view.employee = user

        await interaction.response.defer()


# =========================================================
# ВЫБОР ЗВАНИЯ
# =========================================================

class RankSelect(discord.ui.Select):

    def __init__(self):

        options = [
            discord.SelectOption(
                label=rank,
                value=rank
            )
            for rank in RANK_NAMES
        ]

        super().__init__(
            placeholder="📈 Выберите звание, на которое повысить",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):

        self.view.new_rank = self.values[0]

        await interaction.response.defer()


# =========================================================
# МОДАЛЬНОЕ ОКНО
# =========================================================

class PromotionModal(discord.ui.Modal):

    def __init__(self, employee, new_rank):
        super().__init__(
            title="📋 Заявка на повышение"
        )

        self.employee = employee
        self.new_rank = new_rank

        self.certificate_number = discord.ui.TextInput(
            label="🪪 Номер удостоверения",
            placeholder="Введите номер удостоверения",
            required=True,
            max_length=100
        )

        self.reason = discord.ui.TextInput(
            label="📝 Причина повышения",
            placeholder="Введите причину повышения",
            required=True,
            style=discord.TextStyle.paragraph,
            max_length=1000
        )

        self.add_item(self.certificate_number)
        self.add_item(self.reason)

    async def on_submit(self, interaction: discord.Interaction):

        guild = interaction.guild

        if guild is None:
            await interaction.response.send_message(
                "❌ Сервер не найден.",
                ephemeral=True
            )
            return

        approval_channel = guild.get_channel(
            PROMOTION_APPROVAL_CHANNEL_ID
        )

        if approval_channel is None:
            await interaction.response.send_message(
                "❌ Канал рассмотрения заявок не найден.",
                ephemeral=True
            )
            return

        created_at = current_time().isoformat()

        db = get_db()

        cursor = db.execute("""
            INSERT INTO promotion_requests (
                guild_id,
                employee_id,
                employee_name,
                submitted_by,
                submitted_by_name,
                certificate_number,
                new_rank,
                reason,
                status,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            guild.id,
            self.employee.id,
            self.employee.display_name,
            interaction.user.id,
            interaction.user.display_name,
            self.certificate_number.value,
            self.new_rank,
            self.reason.value,
            "pending",
            created_at
        ))

        request_id = cursor.lastrowid

        db.commit()
        db.close()

        # =================================================
        # EMBED ЗАЯВКИ
        # =================================================

        embed = discord.Embed(
            title=f"📈 ЗАЯВКА НА ПОВЫШЕНИЕ №{request_id}",
            description="Новая заявка ожидает рассмотрения.",
            color=discord.Color.orange(),
            timestamp=created_at_to_datetime(created_at)
        )

        embed.add_field(
            name="👤 Сотрудник",
            value=(
                f"{self.employee.mention}\n"
                f"`{self.employee.display_name}`"
            ),
            inline=False
        )

        embed.add_field(
            name="📈 На какое звание",
            value=f"**{self.new_rank}**",
            inline=False
        )

        embed.add_field(
            name="🪪 Номер удостоверения",
            value=self.certificate_number.value,
            inline=False
        )

        embed.add_field(
            name="📝 Причина повышения",
            value=self.reason.value,
            inline=False
        )

        embed.add_field(
            name="👮 Заявку подал",
            value=interaction.user.mention,
            inline=False
        )

        embed.add_field(
            name="📌 Статус",
            value="🟠 На рассмотрении",
            inline=False
        )

        embed.set_footer(
            text="После одобрения роль выдаётся старшим составом вручную."
        )

        # =================================================
        # ТЕГ СТАРШЕГО СОСТАВА
        # =================================================

        senior_role = guild.get_role(SENIOR_ROLE_ID)

        if senior_role:
            mention = senior_role.mention
        else:
            mention = "⚠️ Старший состав"

        message = await approval_channel.send(
            content=mention,
            embed=embed,
            view=PromotionReviewView(request_id),
            allowed_mentions=discord.AllowedMentions(
                roles=True
            )
        )

        # Сохраняем ID сообщения
        db = get_db()

        db.execute("""
            UPDATE promotion_requests
            SET review_channel_id = ?,
                review_message_id = ?
            WHERE id = ?
        """, (
            approval_channel.id,
            message.id,
            request_id
        ))

        db.commit()
        db.close()

        await interaction.response.send_message(
            f"✅ Заявка №{request_id} успешно отправлена "
            f"старшему составу.",
            ephemeral=True
        )


def created_at_to_datetime(value):
    return datetime.fromisoformat(value)


# =========================================================
# МЕНЮ ЗАЯВКИ
# =========================================================

class PromotionApplicationView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=300)

        self.employee = None
        self.new_rank = None

        self.add_item(EmployeeSelect())
        self.add_item(RankSelect())

    @discord.ui.button(
        label="📨 Отправить заявку",
        style=discord.ButtonStyle.success
    )
    async def submit_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        if self.employee is None:
            await interaction.response.send_message(
                "❌ Выберите сотрудника.",
                ephemeral=True
            )
            return

        if self.new_rank is None:
            await interaction.response.send_message(
                "❌ Выберите звание.",
                ephemeral=True
            )
            return

        await interaction.response.send_modal(
            PromotionModal(
                self.employee,
                self.new_rank
            )
        )


# =========================================================
# ПАНЕЛЬ В КАНАЛЕ
# =========================================================

class PromotionPanelView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="📈 Подать на повышение",
        style=discord.ButtonStyle.primary,
        custom_id="promotion_open_application"
    )
    async def open_application(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        await interaction.response.send_message(
            "## 📋 Заявка на повышение\n\n"
            "**Заполните заявку:**\n\n"
            "1. 👤 Выберите сотрудника\n"
            "2. 📈 Выберите звание, на которое повысить\n"
            "3. 🪪 Укажите номер удостоверения\n"
            "4. 📝 Укажите причину\n\n"
            "После заполнения нажмите **📨 Отправить заявку**.",
            view=PromotionApplicationView(),
            ephemeral=True
        )


# =========================================================
# КНОПКИ ОДОБРЕНИЯ / ОТКЛОНЕНИЯ
# =========================================================

class PromotionReviewView(discord.ui.View):

    def __init__(self, request_id):
        super().__init__(timeout=None)

        self.request_id = request_id

        self.approve_button.custom_id = (
            f"promotion_approve_{request_id}"
        )

        self.reject_button.custom_id = (
            f"promotion_reject_{request_id}"
        )

    async def check_senior(
        self,
        interaction: discord.Interaction
    ):

        if not isinstance(interaction.user, discord.Member):
            return False

        if not is_senior(interaction.user):

            await interaction.response.send_message(
                "❌ Одобрять и отклонять заявки может "
                "только старший состав.",
                ephemeral=True
            )

            return False

        return True

    # =====================================================
    # ОДОБРИТЬ
    # =====================================================

    @discord.ui.button(
        label="✅ Одобрить",
        style=discord.ButtonStyle.success
    )
    async def approve_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        if not await self.check_senior(interaction):
            return

        request = get_request(self.request_id)

        if request is None:
            await interaction.response.send_message(
                "❌ Заявка не найдена.",
                ephemeral=True
            )
            return

        if request[9] != "pending":
            await interaction.response.send_message(
                "❌ Эта заявка уже была обработана.",
                ephemeral=True
            )
            return

        db = get_db()

        db.execute("""
            UPDATE promotion_requests
            SET
                status = 'approved',
                reviewed_at = ?,
                reviewed_by = ?,
                reviewed_by_name = ?
            WHERE id = ?
        """, (
            current_time().isoformat(),
            interaction.user.id,
            interaction.user.display_name,
            self.request_id
        ))

        db.commit()
        db.close()

        await self.finish_request(
            interaction,
            approved=True
        )

    # =====================================================
    # ОТКЛОНИТЬ
    # =====================================================

    @discord.ui.button(
        label="❌ Отклонить",
        style=discord.ButtonStyle.danger
    )
    async def reject_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        if not await self.check_senior(interaction):
            return

        request = get_request(self.request_id)

        if request is None:
            await interaction.response.send_message(
                "❌ Заявка не найдена.",
                ephemeral=True
            )
            return

        if request[9] != "pending":
            await interaction.response.send_message(
                "❌ Эта заявка уже была обработана.",
                ephemeral=True
            )
            return

        db = get_db()

        db.execute("""
            UPDATE promotion_requests
            SET
                status = 'rejected',
                reviewed_at = ?,
                reviewed_by = ?,
                reviewed_by_name = ?
            WHERE id = ?
        """, (
            current_time().isoformat(),
            interaction.user.id,
            interaction.user.display_name,
            self.request_id
        ))

        db.commit()
        db.close()

        await self.finish_request(
            interaction,
            approved=False
        )

    # =====================================================
    # ЗАВЕРШЕНИЕ
    # =====================================================

    async def finish_request(
        self,
        interaction,
        approved
    ):

        request = get_request(self.request_id)

        if approved:
            status_text = "✅ Одобрено"
            color = discord.Color.green()
        else:
            status_text = "❌ Отклонено"
            color = discord.Color.red()

        embed = discord.Embed(
            title=f"📈 ЗАЯВКА НА ПОВЫШЕНИЕ №{self.request_id}",
            color=color
        )

        embed.add_field(
            name="👤 Сотрудник",
            value=(
                f"<@{request[2]}>\n"
                f"`{request[3]}`"
            ),
            inline=False
        )

        embed.add_field(
            name="📈 На какое звание",
            value=f"**{request[7]}**",
            inline=False
        )

        embed.add_field(
            name="🪪 Номер удостоверения",
            value=request[6],
            inline=False
        )

        embed.add_field(
            name="📝 Причина повышения",
            value=request[8],
            inline=False
        )

        embed.add_field(
            name="👮 Заявку подал",
            value=f"<@{request[4]}>",
            inline=False
        )

        embed.add_field(
            name="📌 Статус",
            value=status_text,
            inline=False
        )

        embed.add_field(
            name="👨‍⚖️ Рассмотрел",
            value=interaction.user.mention,
            inline=False
        )

        embed.set_footer(
            text="Роли Discord бот не изменяет."
        )

        # Отключаем обе кнопки
        for item in self.children:
            item.disabled = True

        await interaction.response.edit_message(
            embed=embed,
            view=self
        )


# =========================================================
# КОМАНДА СОЗДАНИЯ ПАНЕЛИ
# =========================================================

@bot.tree.command(
    name="setup_promotions",
    description="Создать панель заявок на повышение"
)
@app_commands.guilds(
    discord.Object(id=GUILD_ID)
)
@app_commands.checks.has_permissions(
    administrator=True
)
async def setup_promotions(
    interaction: discord.Interaction
):

    channel = interaction.guild.get_channel(
        PROMOTION_PANEL_CHANNEL_ID
    )

    if channel is None:
        await interaction.response.send_message(
            "❌ Канал панели не найден.",
            ephemeral=True
        )
        return

    embed = discord.Embed(
        title="📋 СПИСКИ НА ПОВЫШЕНИЯ",
        description=(
            "Здесь сотрудники ГИБДД могут оформить "
            "заявку на повышение.\n\n"

            "**Для подачи заявки нажмите кнопку ниже.**\n\n"

            "После отправки заявка автоматически попадёт "
            "старшему составу на рассмотрение.\n\n"

            "⚠️ **Важно:** бот не выдаёт и не изменяет "
            "роли Discord. После одобрения необходимую "
            "роль вручную выдаёт старший состав."
        ),
        color=discord.Color.blue()
    )

    embed.add_field(
        name="📋 В заявке необходимо указать",
        value=(
            "👤 Сотрудника\n"
            "📈 Звание, на которое повысить\n"
            "🪪 Номер удостоверения\n"
            "📝 Причину повышения"
        ),
        inline=False
    )

    await channel.send(
        embed=embed,
        view=PromotionPanelView()
    )

    await interaction.response.send_message(
        "✅ Панель заявок создана.",
        ephemeral=True
    )


# =========================================================
# READY
# =========================================================

@bot.event
async def on_ready():

    init_database()

    # Постоянная кнопка панели
    bot.add_view(
        PromotionPanelView()
    )

    # Восстанавливаем кнопки заявок после перезапуска
    db = get_db()

    cursor = db.execute("""
        SELECT id, review_message_id
        FROM promotion_requests
        WHERE status = 'pending'
        AND review_message_id IS NOT NULL
    """)

    pending_requests = cursor.fetchall()

    db.close()

    for request_id, message_id in pending_requests:

        try:
            bot.add_view(
                PromotionReviewView(request_id),
                message_id=message_id
            )

        except Exception as error:
            print(
                f"Ошибка восстановления заявки "
                f"№{request_id}: {error}"
            )

    try:

        guild = discord.Object(
            id=GUILD_ID
        )

        synced = await bot.tree.sync(
            guild=guild
        )

        print(
            f"Синхронизировано команд: {len(synced)}"
        )

    except Exception as error:

        print(
            f"Ошибка синхронизации команд: {error}"
        )

    print(
        f"Бот запущен: {bot.user}"
    )


# =========================================================
# ЗАПУСК
# =========================================================

bot.run(TOKEN)