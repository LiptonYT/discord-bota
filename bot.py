import os
from datetime import datetime, timezone

import discord
from discord.ext import commands
from discord import app_commands


# ============================================================
# НАСТРОЙКИ
# ============================================================

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError(
        "DISCORD_TOKEN не задан. "
        "Добавь переменную DISCORD_TOKEN в настройках хостинга."
    )

GUILD_ID = 1533075462383730838
KADRO_PANEL_CHANNEL_ID = 1533076140552491018
KADRO_LOG_CHANNEL_ID = 1533076137209495642

SENIOR_ROLE_ID = 1533075692785504327

FIRED_ROLE_ID = 1533075835097976893
CITIZEN_ROLE_ID = 1533075845663690842
BLACKLIST_ROLE_ID = 1533075833856458972


# ============================================================
# ЗВАНИЯ
# ============================================================

RANKS = {
    "Рядовой": [
        1533075782790807682,
        1533075727241576619,
        1533075731054071959,
        1533075743347572786,
        1533075745751175299,
        1533075784858865704,
        1533075786175746108,
        1533075845663690842,
        1533075702432403456,
    ],

    "Младший сержант": [
        1533075781629251735,
        1533075725983285298,
        1533075731054071959,
        1533075743347572786,
        1533075745751175299,
        1533075784858865704,
        1533075786175746108,
        1533075845663690842,
        1533075702432403456,
    ],

    "Сержант": [
        1533075780312236082,
        1533075786175746108,
        1533075784858865704,
        1533075745751175299,
        1533075731054071959,
        1533075739631550494,
        1533075722330046484,
        1533075702432403456,
    ],

    "Старший сержант": [
        1533075778399637674,
        1533075786175746108,
        1533075784858865704,
        1533075745751175299,
        1533075731054071959,
        1533075739631550494,
        1533075722330046484,
        1533075702432403456,
    ],

    "Старшина": [
        1533075777179095212,
        1533075786175746108,
        1533075784858865704,
        1533075745751175299,
        1533075739631550494,
        1533075702432403456,
    ],

    "Прапорщик": [
        1533075775777931385,
        1533075786175746108,
        1533075784858865704,
        1533075745751175299,
        1533075739631550494,
        1533075702432403456,
    ],

    "Ст прапорщик": [
        1533075774134026350,
        1533075786175746108,
        1533075784858865704,
        1533075745751175299,
        1533075739631550494,
        1533075702432403456,
    ],

    "Младший лейтенант": [
        1533075772950974474,
        1533075786175746108,
        1533075784858865704,
        1533075745751175299,
        1533075739631550494,
        1533075702432403456,
    ],

    "Лейтенант": [
        1533075771801866421,
        1533075786175746108,
        1533075784858865704,
        1533075745751175299,
        1533075731054071959,
        1533075739631550494,
        1533075702432403456,
    ],

    "Старший лейтенант": [
        1533075769881002036,
        1533075786175746108,
        1533075784858865704,
        1533075745751175299,
        1533075731054071959,
        1533075739631550494,
        1533075702432403456,
    ],

    "Капитан": [
        1533075768760991934,
        1533075786175746108,
        1533075784858865704,
        1533075745751175299,
        1533075731054071959,
        1533075739631550494,
        1533075702432403456,
    ],

    "Майор": [
        1533075759583723681,
        1533075786175746108,
        1533075784858865704,
        1533075745751175299,
        1533075731054071959,
        1533075739631550494,
        1533075692785504327,
        1533075702432403456,
    ],

    "Подполковник": [
        1533075757608337538,
        1533075786175746108,
        1533075784858865704,
        1533075745751175299,
        1533075731054071959,
        1533075739631550494,
        1533075692785504327,
        1533075695318732941,
        1533075702432403456,
    ],

    "Полковник": [
        1533075756031279318,
        1533075786175746108,
        1533075784858865704,
        1533075745751175299,
        1533075731054071959,
        1533075739631550494,
        1533075692785504327,
        1533075695318732941,
        1533075702432403456,
    ],

    "Генерал-майор полиции": [
        1533075648577540238,
        1533075786175746108,
        1533075784858865704,
        1533075745751175299,
        1533075731054071959,
        1533075692785504327,
        1533075695318732941,
        1533075754898690171,
        1533075650112655370,
        1533075664494657739,
        1533075653887525046,
        1533075732152975431,
    ],

    "Генерал-лейтенант полиции": [
        1533075752512258099,
        1533075786175746108,
        1533075784858865704,
        1533075745751175299,
        1533075731054071959,
        1533075692785504327,
        1533075695318732941,
        1533075650112655370,
        1533075664494657739,
        1533075653887525046,
        1533075732152975431,
    ],

    "Генерал-полковник полиции": [
        1533075750301732864,
        1533075786175746108,
        1533075784858865704,
        1533075745751175299,
        1533075731054071959,
        1533075692785504327,
        1533075695318732941,
        1533075664494657739,
        1533075653887525046,
        1533075732152975431,
    ],

    "Генерал полиции Российской Федерации": [
        1533075748292661380,
        1533075786175746108,
        1533075784858865704,
        1533075745751175299,
        1533075731054071959,
        1533075692785504327,
        1533075695318732941,
        1533075750301732864,
        1533075664494657739,
        1533075653887525046,
        1533075732152975431,
    ],
}


# ============================================================
# ОТДЕЛЫ
# ============================================================

DEPARTMENT_ROLES = {
    "ОСБ": [
        1533075733314932848,
        1533075710279815390,
        1533075702432403456,
    ],

    "ЦППС": [
        1533075714054684814,
        1533075735462412428,
        1533075702432403456,
    ],

    "1 батальон": [
        1533075722330046484,
        1533075739631550494,
        1533075702432403456,
    ],

    "2 батальон": [
        1533075722330046484,
        1533075740931788910,
        1533075702432403456,
    ],

    "3 батальон": [
        1533075742127034559,
        1533075722330046484,
        1533075702432403456,
    ],
}


# ============================================================
# СТАТУСЫ
# ============================================================

DISMISS_STATUSES = {
    "Уволен": [
        CITIZEN_ROLE_ID,
        FIRED_ROLE_ID,
    ],

    "Чёрный список": [
        CITIZEN_ROLE_ID,
        BLACKLIST_ROLE_ID,
    ],
}


# ============================================================
# BOT
# ============================================================

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


# ============================================================
# ДОСТУП
# ============================================================

def has_senior_access(
    member: discord.Member
) -> bool:

    if member.guild_permissions.administrator:
        return True

    return any(
        role.id == SENIOR_ROLE_ID
        for role in member.roles
    )


# ============================================================
# ОБНОВЛЕНИЕ УЧАСТНИКА
# ============================================================

async def refresh_member(
    guild: discord.Guild,
    member: discord.Member
) -> discord.Member:

    try:
        return await guild.fetch_member(
            member.id
        )

    except (
        discord.HTTPException,
        discord.NotFound
    ):
        return member


# ============================================================
# ID РОЛЕЙ
# ============================================================

def get_all_rank_ids():

    result = set()

    for role_ids in RANKS.values():

        for role_id in role_ids:
            result.add(
                int(role_id)
            )

    return result


def get_all_department_ids():

    result = set()

    for role_ids in DEPARTMENT_ROLES.values():

        for role_id in role_ids:
            result.add(
                int(role_id)
            )

    return result


def get_all_status_ids():

    result = set()

    for role_ids in DISMISS_STATUSES.values():

        for role_id in role_ids:

            role_id = int(role_id)

            if role_id != 0:
                result.add(role_id)

    return result


# ============================================================
# РОЛИ
# ============================================================

def resolve_roles(
    guild: discord.Guild,
    role_ids
):

    roles = []

    for role_id in role_ids:

        role_id = int(role_id)

        if role_id == 0:

            raise RuntimeError(
                "Указан пустой ID роли."
            )

        role = guild.get_role(
            role_id
        )

        if role is None:

            raise RuntimeError(
                f"Роль `{role_id}` не найдена на сервере."
            )

        roles.append(role)

    return list({
        role.id: role
        for role in roles
    }.values())


# ============================================================
# ИЕРАРХИЯ БОТА
# ============================================================

def check_bot_can_manage_roles(
    guild: discord.Guild,
    roles
):

    bot_member = guild.me

    if bot_member is None:

        raise RuntimeError(
            "Не удалось определить роль бота."
        )

    for role in roles:

        if role is None:
            continue

        if role.is_default():
            continue

        if role >= bot_member.top_role:

            raise RuntimeError(
                f"Бот не может управлять ролью "
                f"**{role.name}** (`{role.id}`).\n\n"
                "Подними главную роль бота выше этой роли."
            )

        if not role.is_assignable():

            raise RuntimeError(
                f"Роль **{role.name}** нельзя выдать или снять ботом."
            )


# ============================================================
# ОПРЕДЕЛЕНИЕ ЗВАНИЯ
# ============================================================

def get_actual_rank(
    member: discord.Member
):

    member_role_ids = {
        int(role.id)
        for role in member.roles
    }

    found_ranks = []

    for rank_name, role_ids in RANKS.items():

        if not role_ids:
            continue

        primary_role_id = int(
            role_ids[0]
        )

        if primary_role_id in member_role_ids:

            found_ranks.append(
                rank_name
            )

    if not found_ranks:
        return None

    rank_order = list(
        RANKS.keys()
    )

    return max(
        found_ranks,
        key=rank_order.index
    )


# ============================================================
# ПРОВЕРКА ЗВАНИЯ
# ============================================================

def validate_current_rank(
    member: discord.Member,
    selected_rank: str
):

    if selected_rank not in RANKS:

        raise RuntimeError(
            f"Звание `{selected_rank}` не найдено."
        )

    member_role_ids = {
        int(role.id)
        for role in member.roles
    }

    primary_role_id = int(
        RANKS[selected_rank][0]
    )

    if primary_role_id not in member_role_ids:

        actual_rank = get_actual_rank(
            member
        )

        if actual_rank is None:
            actual_rank = "не определено"

        raise RuntimeError(
            f"❌ У сотрудника другое звание.\n\n"
            f"Вы выбрали: **{selected_rank}**\n"
            f"Фактически: **{actual_rank}**\n\n"
            "⚠️ Роли сотрудника не изменены."
        )

    return True


# ============================================================
# ОПРЕДЕЛЕНИЕ ОТДЕЛА
# ============================================================

def get_actual_department(
    member: discord.Member
):

    member_role_ids = {
        int(role.id)
        for role in member.roles
    }

    full_matches = []

    for department_name, role_ids in DEPARTMENT_ROLES.items():

        department_ids = {
            int(role_id)
            for role_id in role_ids
        }

        if department_ids.issubset(
            member_role_ids
        ):

            full_matches.append(
                department_name
            )

    if len(full_matches) == 1:
        return full_matches[0]

    if len(full_matches) > 1:

        for department_name in full_matches:

            role_ids = {
                int(role_id)
                for role_id in DEPARTMENT_ROLES[
                    department_name
                ]
            }

            other_ids = set()

            for other_department in full_matches:

                if other_department == department_name:
                    continue

                other_ids.update(
                    int(role_id)
                    for role_id in DEPARTMENT_ROLES[
                        other_department
                    ]
                )

            unique_ids = (
                role_ids - other_ids
            )

            if unique_ids & member_role_ids:
                return department_name

        return {
            "error": "multiple",
            "departments": full_matches
        }

    # Дополнительная проверка уникальных ролей
    candidates = []

    for department_name, role_ids in DEPARTMENT_ROLES.items():

        department_ids = {
            int(role_id)
            for role_id in role_ids
        }

        other_ids = set()

        for other_department, other_role_ids in DEPARTMENT_ROLES.items():

            if other_department == department_name:
                continue

            other_ids.update(
                int(role_id)
                for role_id in other_role_ids
            )

        unique_ids = (
            department_ids - other_ids
        )

        if unique_ids & member_role_ids:
            candidates.append(
                department_name
            )

    if len(candidates) == 1:
        return candidates[0]

    if len(candidates) > 1:

        return {
            "error": "multiple",
            "departments": candidates
        }

    return None


# ============================================================
# ПРОВЕРКА ОТДЕЛА
# ============================================================

def validate_current_department(
    member: discord.Member,
    selected_department: str
):

    actual_department = get_actual_department(
        member
    )

    if actual_department is None:

        raise RuntimeError(
            "❌ Не удалось определить отдел сотрудника.\n\n"
            f"Вы выбрали: **{selected_department}**\n\n"
            "⚠️ Роли сотрудника не изменены."
        )

    if isinstance(
        actual_department,
        dict
    ):

        if selected_department in actual_department["departments"]:
            return True

        raise RuntimeError(
            "❌ Выбранный отдел не соответствует ролям сотрудника.\n\n"
            f"Вы выбрали: **{selected_department}**\n"
            f"Найдено: **{', '.join(actual_department['departments'])}**\n\n"
            "⚠️ Роли сотрудника не изменены."
        )

    if actual_department != selected_department:

        raise RuntimeError(
            f"❌ У сотрудника другой отдел.\n\n"
            f"Вы выбрали: **{selected_department}**\n"
            f"Фактически: **{actual_department}**\n\n"
            "⚠️ Роли сотрудника не изменены."
        )

    return True


# ============================================================
# СМЕНА ЗВАНИЯ
#
# НОВОЕ ЗВАНИЕ:
#   + выдаём ТОЛЬКО роли звания
#   - забираем старые роли звания
#   = роли отдела НЕ ТРОГАЕМ
# ============================================================

async def change_rank(
    member: discord.Member,
    current_rank: str,
    new_rank: str
):

    guild = member.guild

    if current_rank not in RANKS:

        raise RuntimeError(
            f"Звание `{current_rank}` не найдено."
        )

    if new_rank not in RANKS:

        raise RuntimeError(
            f"Звание `{new_rank}` не найдено."
        )

    if current_rank == new_rank:

        raise RuntimeError(
            "Текущее и новое звание совпадают."
        )

    member = await refresh_member(
        guild,
        member
    )

    # --------------------------------------------------------
    # ВСЕ РОЛИ ОТДЕЛОВ
    # --------------------------------------------------------

    department_role_ids = get_all_department_ids()

    # --------------------------------------------------------
    # РОЛИ НОВОГО ЗВАНИЯ
    #
    # ВАЖНО:
    # Всё, что является ролью отдела,
    # здесь исключается.
    # --------------------------------------------------------

    configured_new_rank_ids = {
        int(role_id)
        for role_id in RANKS[new_rank]
    }

    new_rank_ids = {
        role_id
        for role_id in configured_new_rank_ids
        if role_id not in department_role_ids
    }

    if not new_rank_ids:

        raise RuntimeError(
            f"Для звания **{new_rank}** "
            "не найдены отдельные роли звания."
        )

    new_roles = resolve_roles(
        guild,
        new_rank_ids
    )

    # --------------------------------------------------------
    # ПРОВЕРЯЕМ НОВЫЕ РОЛИ
    # --------------------------------------------------------

    check_bot_can_manage_roles(
        guild,
        new_roles
    )

    # --------------------------------------------------------
    # ВЫДАЁМ НОВЫЕ РОЛИ
    # --------------------------------------------------------

    roles_to_add = [
        role
        for role in new_roles
        if role not in member.roles
    ]

    if roles_to_add:

        try:

            await member.add_roles(
                *roles_to_add,
                reason=(
                    f"Повышение/понижение звания: "
                    f"{current_rank} → {new_rank}"
                )
            )

        except discord.Forbidden:

            raise RuntimeError(
                "Не удалось выдать новые роли звания.\n\n"
                "Проверь иерархию ролей бота."
            )

    member = await refresh_member(
        guild,
        member
    )

    # --------------------------------------------------------
    # ВСЕ РОЛИ, КОТОРЫЕ ИСПОЛЬЗУЮТСЯ В RANKS
    # --------------------------------------------------------

    all_rank_role_ids = get_all_rank_ids()

    # --------------------------------------------------------
    # СТАРЫЕ РОЛИ ЗВАНИЯ
    #
    # РОЛИ ОТДЕЛОВ ИСКЛЮЧАЕМ
    # --------------------------------------------------------

    roles_to_remove = [
        role
        for role in member.roles
        if (
            int(role.id) in all_rank_role_ids
            and int(role.id) not in new_rank_ids
            and int(role.id) not in department_role_ids
        )
    ]

    roles_to_remove = list({
        role.id: role
        for role in roles_to_remove
    }.values())

    if roles_to_remove:

        check_bot_can_manage_roles(
            guild,
            roles_to_remove
        )

        try:

            await member.remove_roles(
                *roles_to_remove,
                reason=(
                    f"Снятие старых ролей звания: "
                    f"{current_rank} → {new_rank}"
                )
            )

        except discord.Forbidden:

            raise RuntimeError(
                "Новое звание выдано, "
                "но старые роли снять не удалось.\n\n"
                "Проверь иерархию ролей бота."
            )

    return await refresh_member(
        guild,
        member
    )


# ============================================================
# ПЕРЕВОД ОТДЕЛА
#
# СТАРЫЙ ОТДЕЛ:
#   - снимаем
#
# НОВЫЙ ОТДЕЛ:
#   + выдаём
#
# ЗВАНИЕ:
#   не меняем
# ============================================================

async def change_department(
    member: discord.Member,
    current_department: str,
    new_department: str
):

    guild = member.guild

    if current_department not in DEPARTMENT_ROLES:

        raise RuntimeError(
            f"Отдел `{current_department}` не найден."
        )

    if new_department not in DEPARTMENT_ROLES:

        raise RuntimeError(
            f"Отдел `{new_department}` не найден."
        )

    if current_department == new_department:

        raise RuntimeError(
            "Текущий и новый отдел совпадают."
        )

    old_roles = resolve_roles(
        guild,
        DEPARTMENT_ROLES[current_department]
    )

    new_roles = resolve_roles(
        guild,
        DEPARTMENT_ROLES[new_department]
    )

    check_bot_can_manage_roles(
        guild,
        old_roles + new_roles
    )

    # --------------------------------------------------------
    # ВЫДАЁМ НОВЫЙ ОТДЕЛ
    # --------------------------------------------------------

    roles_to_add = [
        role
        for role in new_roles
        if role not in member.roles
    ]

    if roles_to_add:

        try:

            await member.add_roles(
                *roles_to_add,
                reason=(
                    f"Перевод: "
                    f"{current_department} → "
                    f"{new_department}"
                )
            )

        except discord.Forbidden:

            raise RuntimeError(
                "Не удалось выдать роли нового отдела.\n\n"
                "Проверь иерархию ролей бота."
            )

    member = await refresh_member(
        guild,
        member
    )

    # --------------------------------------------------------
    # СНИМАЕМ СТАРЫЙ ОТДЕЛ
    #
    # Общие роли двух отделов оставляем.
    # --------------------------------------------------------

    new_role_ids = {
        int(role.id)
        for role in new_roles
    }

    roles_to_remove = [
        role
        for role in old_roles
        if (
            role in member.roles
            and int(role.id) not in new_role_ids
        )
    ]

    if roles_to_remove:

        check_bot_can_manage_roles(
            guild,
            roles_to_remove
        )

        try:

            await member.remove_roles(
                *roles_to_remove,
                reason=(
                    f"Снятие отдела: "
                    f"{current_department} → "
                    f"{new_department}"
                )
            )

        except discord.Forbidden:

            raise RuntimeError(
                "Новый отдел выдан, "
                "но старый отдел снять не удалось."
            )

    return await refresh_member(
        guild,
        member
    )


# ============================================================
# УВОЛЬНЕНИЕ — СТАТУС
# ============================================================

async def apply_dismiss_status(
    member: discord.Member,
    status_name: str
):

    guild = member.guild

    if status_name not in DISMISS_STATUSES:

        raise RuntimeError(
            f"Статус `{status_name}` не найден."
        )

    target_roles = resolve_roles(
        guild,
        DISMISS_STATUSES[status_name]
    )

    all_status_roles = resolve_roles(
        guild,
        get_all_status_ids()
    )

    check_bot_can_manage_roles(
        guild,
        all_status_roles + target_roles
    )

    target_ids = {
        int(role.id)
        for role in target_roles
    }

    roles_to_remove = [
        role
        for role in all_status_roles
        if (
            role in member.roles
            and int(role.id) not in target_ids
        )
    ]

    if roles_to_remove:

        try:

            await member.remove_roles(
                *roles_to_remove,
                reason="Удаление старого статуса"
            )

        except discord.Forbidden:

            raise RuntimeError(
                "Не удалось снять старый статус."
            )

    roles_to_add = [
        role
        for role in target_roles
        if role not in member.roles
    ]

    if roles_to_add:

        try:

            await member.add_roles(
                *roles_to_add,
                reason=(
                    f"Статус после увольнения: "
                    f"{status_name}"
                )
            )

        except discord.Forbidden:

            raise RuntimeError(
                f"Не удалось выдать статус `{status_name}`."
            )

    return await refresh_member(
        guild,
        member
    )


# ============================================================
# УВОЛЬНЕНИЕ
# ============================================================

async def dismiss_member(
    member: discord.Member,
    current_rank: str,
    current_department: str,
    status_name: str
):

    guild = member.guild

    all_rank_roles = resolve_roles(
        guild,
        get_all_rank_ids()
    )

    all_department_roles = resolve_roles(
        guild,
        get_all_department_ids()
    )

    all_staff_roles = list({
        role.id: role
        for role in (
            all_rank_roles +
            all_department_roles
        )
    }.values())

    roles_to_remove = [
        role
        for role in all_staff_roles
        if role in member.roles
    ]

    if roles_to_remove:

        check_bot_can_manage_roles(
            guild,
            roles_to_remove
        )

        try:

            await member.remove_roles(
                *roles_to_remove,
                reason=(
                    f"Увольнение | "
                    f"{current_rank} | "
                    f"{current_department}"
                )
            )

        except discord.Forbidden:

            raise RuntimeError(
                "Не удалось снять кадровые роли."
            )

    member = await refresh_member(
        guild,
        member
    )

    return await apply_dismiss_status(
        member,
        status_name
    )


# ============================================================
# ЛОГ
# ============================================================

async def send_log(
    guild: discord.Guild,
    action,
    employee,
    executor,
    current_rank=None,
    new_rank=None,
    current_department=None,
    new_department=None,
    reason=None,
    dismiss_status=None
):

    channel = guild.get_channel(
        KADRO_LOG_CHANNEL_ID
    )

    if channel is None:

        try:

            channel = await guild.fetch_channel(
                KADRO_LOG_CHANNEL_ID
            )

        except Exception as error:

            print(
                f"⚠️ Канал логов не найден: {error}"
            )

            return

    embed = discord.Embed(
        title="📋 КАДРОВОЕ ДЕЙСТВИЕ",
        color=discord.Color.from_rgb(
            255,
            193,
            7
        ),
        timestamp=datetime.now(
            timezone.utc
        )
    )

    embed.add_field(
        name="👤 Сотрудник",
        value=(
            f"{employee.mention}\n"
            f"`{employee.id}`"
        ),
        inline=False
    )

    embed.add_field(
        name="📌 Действие",
        value=action,
        inline=True
    )

    embed.add_field(
        name="👮 Кадровик",
        value=executor.mention,
        inline=True
    )

    if current_rank:

        embed.add_field(
            name="🎖️ Текущее звание",
            value=current_rank,
            inline=True
        )

    if new_rank:

        embed.add_field(
            name="🎖️ Новое звание",
            value=new_rank,
            inline=True
        )

    if current_department:

        embed.add_field(
            name="🏢 Текущий отдел",
            value=current_department,
            inline=True
        )

    if new_department:

        embed.add_field(
            name="🏢 Новый отдел",
            value=new_department,
            inline=True
        )

    if dismiss_status:

        embed.add_field(
            name="📌 Итоговый статус",
            value=dismiss_status,
            inline=False
        )

    if reason:

        embed.add_field(
            name="📝 Причина",
            value=str(reason)[:1024],
            inline=False
        )

    embed.set_footer(
        text="Аудит Lipton ГИБДД"
    )

    try:

        await channel.send(
            embed=embed
        )

    except Exception as error:

        print(
            f"⚠️ Ошибка отправки лога: {error}"
        )


# ============================================================
# ГЛАВНАЯ ПАНЕЛЬ
# ============================================================

def main_embed():

    embed = discord.Embed(
        title="🛡️ АУДИТ LIPTON ГИБДД",
        description=(
            "## 📋 Кадровая система\n\n"

            "📈 **Повышение**\n"
            "Выдача ролей нового звания и снятие "
            "старых ролей звания.\n\n"

            "📉 **Понижение**\n"
            "Выдача ролей нового звания и снятие "
            "старых ролей звания.\n\n"

            "🔄 **Перевод**\n"
            "Снятие старого отдела и выдача нового.\n\n"

            "🚫 **Увольнение**\n"
            "Снятие кадровых ролей и выдача статуса.\n\n"

            "━━━━━━━━━━━━━━━━━━━━━━\n"

            "🏢 При повышении и понижении "
            "**роли отдела сохраняются**.\n\n"

            "🔐 Доступ: **роль старшего состава**"
        ),
        color=discord.Color.from_rgb(
            30,
            30,
            35
        )
    )

    embed.set_footer(
        text="Аудит Lipton ГИБДД"
    )

    return embed


# ============================================================
# OPTIONS
# ============================================================

def rank_options(
    exclude=None
):

    return [
        discord.SelectOption(
            label=rank,
            value=rank
        )
        for rank in RANKS
        if rank != exclude
    ]


def department_options(
    exclude=None
):

    return [
        discord.SelectOption(
            label=name,
            value=name
        )
        for name in DEPARTMENT_ROLES
        if name != exclude
    ]


# ============================================================
# POPUP
# ============================================================

class KadroModal(
    discord.ui.Modal
):

    def __init__(
        self,
        action
    ):

        self.action = action

        title_map = {
            "promote": "📈 Повышение сотрудника",
            "demote": "📉 Понижение сотрудника",
            "transfer": "🔄 Перевод сотрудника",
            "dismiss": "🚫 Увольнение сотрудника",
        }

        super().__init__(
            title=title_map[action],
            timeout=300
        )

        # ----------------------------------------------------
        # СОТРУДНИК
        # ----------------------------------------------------

        self.employee_select = discord.ui.UserSelect(
            custom_id=f"kadro_{action}_employee",
            placeholder="Выберите сотрудника...",
            min_values=1,
            max_values=1,
            required=True
        )

        self.add_item(
            discord.ui.Label(
                text="👤 Сотрудник",
                description="Кого необходимо обработать",
                component=self.employee_select
            )
        )

        # ----------------------------------------------------
        # ТЕКУЩЕЕ ЗВАНИЕ
        # ----------------------------------------------------

        self.current_rank_select = discord.ui.Select(
            custom_id=f"kadro_{action}_current_rank",
            placeholder="Выберите текущее звание...",
            options=rank_options(),
            min_values=1,
            max_values=1,
            required=True
        )

        self.add_item(
            discord.ui.Label(
                text="🎖️ Текущее звание",
                description="Звание сотрудника сейчас",
                component=self.current_rank_select
            )
        )

        # ----------------------------------------------------
        # НОВОЕ ЗВАНИЕ
        # ----------------------------------------------------

        self.new_rank_select = None

        if action in (
            "promote",
            "demote"
        ):

            self.new_rank_select = discord.ui.Select(
                custom_id=f"kadro_{action}_new_rank",
                placeholder="Выберите новое звание...",
                options=rank_options(),
                min_values=1,
                max_values=1,
                required=True
            )

            self.add_item(
                discord.ui.Label(
                    text="🎯 Новое звание",
                    description="Звание после действия",
                    component=self.new_rank_select
                )
            )

        # ----------------------------------------------------
        # ТЕКУЩИЙ ОТДЕЛ
        # ----------------------------------------------------

        self.current_department_select = None

        if action in (
            "transfer",
            "dismiss"
        ):

            self.current_department_select = discord.ui.Select(
                custom_id=f"kadro_{action}_current_department",
                placeholder="Выберите текущий отдел...",
                options=department_options(),
                min_values=1,
                max_values=1,
                required=True
            )

            self.add_item(
                discord.ui.Label(
                    text="🏢 Текущий отдел",
                    description="Отдел сотрудника сейчас",
                    component=self.current_department_select
                )
            )

        # ----------------------------------------------------
        # НОВЫЙ ОТДЕЛ
        # ----------------------------------------------------

        self.new_department_select = None

        if action == "transfer":

            self.new_department_select = discord.ui.Select(
                custom_id="kadro_transfer_new_department",
                placeholder="Выберите новый отдел...",
                options=department_options(),
                min_values=1,
                max_values=1,
                required=True
            )

            self.add_item(
                discord.ui.Label(
                    text="🏢 Новый отдел",
                    description="Отдел после перевода",
                    component=self.new_department_select
            )
            )

        # ----------------------------------------------------
        # СТАТУС
        # ----------------------------------------------------

        self.dismiss_status_select = None

        if action == "dismiss":

            self.dismiss_status_select = discord.ui.Select(
                custom_id="kadro_dismiss_status",
                placeholder="Выберите итоговый статус...",
                options=[
                    discord.SelectOption(
                        label="Уволен",
                        value="Уволен",
                        description="Гражданин + Уволен",
                        emoji="🚫"
                    ),

                    discord.SelectOption(
                        label="Чёрный список",
                        value="Чёрный список",
                        description="Гражданин + Чёрный список",
                        emoji="⛔"
                    )
                ],
                min_values=1,
                max_values=1,
                required=True
            )

            self.add_item(
                discord.ui.Label(
                    text="📌 Итоговый статус",
                    description="Статус после увольнения",
                    component=self.dismiss_status_select
                )
            )

        # ----------------------------------------------------
        # ПРИЧИНА
        # ----------------------------------------------------

        self.reason_input = discord.ui.TextInput(
            custom_id=f"kadro_{action}_reason",
            placeholder="Введите причину...",
            min_length=3,
            max_length=500,
            required=True,
            style=discord.TextStyle.paragraph
        )

        self.add_item(
            discord.ui.Label(
                text="📝 Причина",
                description="Причина кадрового действия",
                component=self.reason_input
            )
        )

    # ========================================================
    # SUBMIT
    # ========================================================

    async def on_submit(
        self,
        interaction: discord.Interaction
    ):

        if not has_senior_access(
            interaction.user
        ):

            await interaction.response.send_message(
                "❌ У вас нет доступа к кадровой системе.",
                ephemeral=True
            )

            return

        try:

            # -------------------------------------------------
            # СОТРУДНИК
            # -------------------------------------------------

            employee = self.employee_select.values[0]

            if not isinstance(
                employee,
                discord.Member
            ):

                employee = interaction.guild.get_member(
                    employee.id
                )

            if employee is None:

                raise RuntimeError(
                    "Сотрудник не найден."
                )

            if employee.bot:

                raise RuntimeError(
                    "Нельзя использовать кадровую систему "
                    "для Discord-бота."
                )

            # -------------------------------------------------
            # ЗНАЧЕНИЯ
            # -------------------------------------------------

            current_rank = (
                self.current_rank_select.values[0]
            )

            reason = str(
                self.reason_input.value
            ).strip()

            if not reason:

                raise RuntimeError(
                    "Причина обязательна."
                )

            new_rank = None
            current_department = None
            new_department = None
            dismiss_status = None

            if self.new_rank_select:

                new_rank = (
                    self.new_rank_select.values[0]
                )

            if self.current_department_select:

                current_department = (
                    self.current_department_select.values[0]
                )

            if self.new_department_select:

                new_department = (
                    self.new_department_select.values[0]
                )

            if self.dismiss_status_select:

                dismiss_status = (
                    self.dismiss_status_select.values[0]
                )

            # -------------------------------------------------
            # СВЕЖИЕ ДАННЫЕ
            # -------------------------------------------------

            employee = await refresh_member(
                interaction.guild,
                employee
            )

            # =================================================
            # ПОВЫШЕНИЕ
            # =================================================

            if self.action == "promote":

                validate_current_rank(
                    employee,
                    current_rank
                )

                employee = await change_rank(
                    employee,
                    current_rank,
                    new_rank
                )

                await send_log(
                    guild=interaction.guild,
                    action="📈 Повышение",
                    employee=employee,
                    executor=interaction.user,
                    current_rank=current_rank,
                    new_rank=new_rank,
                    reason=reason
                )

                result = (
                    "✅ **Аудит оформлен**\n\n"
                    f"👤 Сотрудник: {employee.mention}\n"
                    "📈 Действие: **Повышение**\n"
                    f"🎖️ Было: **{current_rank}**\n"
                    f"🎖️ Стало: **{new_rank}**\n\n"
                    "🏢 Роли отдела сохранены.\n\n"
                    f"📝 Причина:\n{reason}"
                )

            # =================================================
            # ПОНИЖЕНИЕ
            # =================================================

            elif self.action == "demote":

                validate_current_rank(
                    employee,
                    current_rank
                )

                employee = await change_rank(
                    employee,
                    current_rank,
                    new_rank
                )

                await send_log(
                    guild=interaction.guild,
                    action="📉 Понижение",
                    employee=employee,
                    executor=interaction.user,
                    current_rank=current_rank,
                    new_rank=new_rank,
                    reason=reason
                )

                result = (
                    "✅ **Аудит оформлен**\n\n"
                    f"👤 Сотрудник: {employee.mention}\n"
                    "📉 Действие: **Понижение**\n"
                    f"🎖️ Было: **{current_rank}**\n"
                    f"🎖️ Стало: **{new_rank}**\n\n"
                    "🏢 Роли отдела сохранены.\n\n"
                    f"📝 Причина:\n{reason}"
                )

            # =================================================
            # ПЕРЕВОД
            # =================================================

            elif self.action == "transfer":

                validate_current_rank(
                    employee,
                    current_rank
                )

                validate_current_department(
                    employee,
                    current_department
                )

                employee = await change_department(
                    employee,
                    current_department,
                    new_department
                )

                await send_log(
                    guild=interaction.guild,
                    action="🔄 Перевод",
                    employee=employee,
                    executor=interaction.user,
                    current_rank=current_rank,
                    new_rank=current_rank,
                    current_department=current_department,
                    new_department=new_department,
                    reason=reason
                )

                result = (
                    "✅ **Аудит оформлен**\n\n"
                    f"👤 Сотрудник: {employee.mention}\n"
                    "🔄 Действие: **Перевод**\n"
                    f"🎖️ Звание: **{current_rank}**\n"
                    f"🏢 Было: **{current_department}**\n"
                    f"🏢 Стало: **{new_department}**\n\n"
                    f"📝 Причина:\n{reason}"
                )

            # =================================================
            # УВОЛЬНЕНИЕ
            # =================================================

            elif self.action == "dismiss":

                if not dismiss_status:

                    raise RuntimeError(
                        "Не выбран статус увольнения."
                    )

                validate_current_rank(
                    employee,
                    current_rank
                )

                validate_current_department(
                    employee,
                    current_department
                )

                employee = await dismiss_member(
                    employee,
                    current_rank,
                    current_department,
                    dismiss_status
                )

                await send_log(
                    guild=interaction.guild,
                    action="🚫 Увольнение",
                    employee=employee,
                    executor=interaction.user,
                    current_rank=current_rank,
                    current_department=current_department,
                    reason=reason,
                    dismiss_status=dismiss_status
                )

                result = (
                    "✅ **Аудит оформлен**\n\n"
                    f"👤 Сотрудник: {employee.mention}\n"
                    "🚫 Действие: **Увольнение**\n"
                    f"🎖️ Звание: **{current_rank}**\n"
                    f"🏢 Отдел: **{current_department}**\n\n"
                    f"📌 Статус: **{dismiss_status}**\n"
                    "👤 Роль **Гражданин** выдана автоматически.\n\n"
                    f"📝 Причина:\n{reason}"
                )

            else:

                raise RuntimeError(
                    "Неизвестное кадровое действие."
                )

            # -------------------------------------------------
            # ПРИВАТНЫЙ РЕЗУЛЬТАТ
            # -------------------------------------------------

            await interaction.response.send_message(
                result,
                ephemeral=True
            )

        except discord.Forbidden:

            await interaction.response.send_message(
                (
                    "❌ **Недостаточно прав**\n\n"
                    "Бот не может изменить одну или несколько ролей.\n\n"
                    "Проверь иерархию ролей Discord."
                ),
                ephemeral=True
            )

        except RuntimeError as error:

            await interaction.response.send_message(
                (
                    "❌ **Кадровое действие отменено**\n\n"
                    f"{error}"
                ),
                ephemeral=True
            )

        except Exception as error:

            print(
                f"[KADRO ERROR] {repr(error)}"
            )

            await interaction.response.send_message(
                (
                    "❌ **Ошибка кадрового действия**\n\n"
                    "```text\n"
                    f"{str(error)[:3500]}\n"
                    "```"
                ),
                ephemeral=True
            )


# ============================================================
# КНОПКИ ПАНЕЛИ
# ============================================================

class KadroActionButton(
    discord.ui.Button
):

    def __init__(
        self,
        action,
        label,
        emoji,
        style,
        custom_id
    ):

        self.action = action

        super().__init__(
            label=label,
            emoji=emoji,
            style=style,
            custom_id=custom_id
        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        if not has_senior_access(
            interaction.user
        ):

            await interaction.response.send_message(
                "❌ У вас нет доступа к кадровой системе.",
                ephemeral=True
            )

            return

        await interaction.response.send_modal(
            KadroModal(
                self.action
            )
        )


class KadroPanel(
    discord.ui.View
):

    def __init__(self):

        super().__init__(
            timeout=None
        )

        self.add_item(
            KadroActionButton(
                action="promote",
                label="Повышение",
                emoji="📈",
                style=discord.ButtonStyle.success,
                custom_id="kadro_promote"
            )
        )

        self.add_item(
            KadroActionButton(
                action="demote",
                label="Понижение",
                emoji="📉",
                style=discord.ButtonStyle.danger,
                custom_id="kadro_demote"
            )
        )

        self.add_item(
            KadroActionButton(
                action="transfer",
                label="Перевод",
                emoji="🔄",
                style=discord.ButtonStyle.primary,
                custom_id="kadro_transfer"
            )
        )

        self.add_item(
            KadroActionButton(
                action="dismiss",
                label="Увольнение",
                emoji="🚫",
                style=discord.ButtonStyle.secondary,
                custom_id="kadro_dismiss"
            )
        )


# ============================================================
# /SETUP_KADRO
# ============================================================

@bot.tree.command(
    name="setup_kadro",
    description="Установить панель кадрового аудита"
)
@app_commands.guilds(
    discord.Object(
        id=GUILD_ID
    )
)
async def setup_kadro(
    interaction: discord.Interaction
):

    if not has_senior_access(
        interaction.user
    ):

        await interaction.response.send_message(
            "❌ У вас нет доступа к кадровой системе.",
            ephemeral=True
        )

        return

    channel = bot.get_channel(
        KADRO_PANEL_CHANNEL_ID
    )

    if channel is None:

        try:

            channel = await bot.fetch_channel(
                KADRO_PANEL_CHANNEL_ID
            )

        except Exception:

            await interaction.response.send_message(
                "❌ Канал кадровой панели не найден.",
                ephemeral=True
            )

            return

    await channel.send(
        embed=main_embed(),
        view=KadroPanel()
    )

    await interaction.response.send_message(
        "✅ Панель кадрового аудита установлена.",
        ephemeral=True
    )


# ============================================================
# READY
# ============================================================

@bot.event
async def on_ready():

    print("=" * 60)
    print("🤖 АУДИТ LIPTON ГИБДД")
    print(f"Бот: {bot.user}")
    print(f"ID: {bot.user.id}")
    print(f"Серверов: {len(bot.guilds)}")
    print("=" * 60)

    if not getattr(
        bot,
        "_kadro_view_added",
        False
    ):

        bot.add_view(
            KadroPanel()
        )

        bot._kadro_view_added = True

    guild = bot.get_guild(
        GUILD_ID
    )

    if guild is None:

        print(
            "❌ Сервер GUILD_ID не найден."
        )

        return

    print(
        f"✅ Сервер: {guild.name}"
    )

    print(
        f"✅ Званий: {len(RANKS)}"
    )

    print(
        f"✅ Отделов: {len(DEPARTMENT_ROLES)}"
    )

    try:

        synced = await bot.tree.sync(
            guild=discord.Object(
                id=GUILD_ID
            )
        )

        print(
            f"✅ Slash-команд синхронизировано: "
            f"{len(synced)}"
        )

    except Exception as error:

        print(
            f"❌ Ошибка синхронизации: {error}"
        )


# ============================================================
# ЗАПУСК ДЛЯ ХОСТИНГА
# ============================================================

if __name__ == "__main__":

    bot.run(
        TOKEN,
        reconnect=True
    )
