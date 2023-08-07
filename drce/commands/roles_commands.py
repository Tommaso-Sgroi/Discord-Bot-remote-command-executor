from abc import ABC

import discord
from discord import Permissions

from drce.commands.commands_archetypes import *


# class MakeRoleCommand(Command):
#     def __init__(self, guild: discord.Guild, name: str, permissions: Permissions):
#         Command.__init__(self, guild)
#         self.name = name
#         self.permission = permissions
#
#     async def run(self):
#         try:
#             await self.guild.create_role(name=self.name, permissions=self.permission)
#         except:
#             print(f"Some error occurred while making {self.name} role")
#             return
#         print(f"successfully made {self.name} role")

class RoleCommand(TargetCommand, ABC):

    def __init__(self, client, guild, roles_id):
        TargetCommand.__init__(self, client, guild, roles_id)

    def get_targets(self, roles_id):
        roles = []
        for guild in self.guild:
            if roles_id == all_:
                roles.extend(guild.roles)
            else:
                for target in roles_id:
                    role = guild.get_role(target)
                    if role is not None:
                        roles.append(role)
        return roles


class DeleteRoleCommand(RoleCommand):

    def __init__(self, client, guild, role_id):
        RoleCommand.__init__(self, client, guild, role_id)

    async def run(self):
        for role in self.target:
            try:
                await role.delete()
                self.log_info(f"successfully deleted {role.name if role is not None else 'None'} " +
                              f"role in guild {role.guild}")
            except Exception as e:
                self.log_error(f'cannot delete role "{role.name if role is not None else "None"} ' +
                               f"role in guild {role.guild}: ", error=e)


class ResetRoleCommand(RoleCommand):

    def __init__(self, client, guild, role_id):
        RoleCommand.__init__(self, client, guild, role_id)

    async def run(self):
        for role in self.target:
            try:
                await role.edit(permissions=Permissions(0).none())
                self.log_info(f"successfully reset \"{role.name}\" in guild \"{role.guild}\"")
            except Exception as e:
                self.log_error(f"cannot reset \"{role.name}\" in guild \"{role.guild}\"", error=e)


class EditRoleCommand(RoleCommand):

    def __init__(self, client, guild, role, permissions: int):
        RoleCommand.__init__(self, client, guild, role)
        self.permissions = permissions

    def __str__(self):
        return RoleCommand.__str__(self) + f'\nWith permission: {self.permissions}'

    def get_permission(self):
        return self.permissions if type(self.permissions) is int else int(self.permissions)

    async def run(self):
        for role in self.target:
            try:
                await role.edit(permissions=Permissions(self.get_permission()))
                self.log_info(f"successfully edited {role.name} in {role.guild} role")
            except Exception as e:
                self.log_error(f'cannot edit role "{role.name} in guild "{role.guild}: ', error=e)


class AddRoleCommand(Command):
    def __init__(self, client, guild, name, permissions: int):
        Command.__init__(self, client, guild)
        self.permissions = permissions
        self.name = name

    async def run(self):
        for guild in self.guild:
            try:
                await guild.create_role(name=self.name,
                                        permissions=discord.Permissions(
                                            self.permissions if type(self.permissions) is int
                                            else int(self.permissions)),
                                        colour=discord.Colour.random())
                self.log_info(f"successfully added new role {self.name} role in {guild}")
            except Exception as e:
                self.log_error(f'error adding new role "{self.name}" in guild {guild}: ', error=e)


class GiveRoleCommand(RoleCommand):
    def __init__(self, client, guild, role, target_user):
        if all_ in target_user:
            self.target_users = all_
        else:
            for i in range(len(target_user)):
                if type(target_user[i]) is str and target_user[i].isnumeric():
                    target_user[i] = int(target_user[i])
            self.target_users = target_user
        self.role_user_list = []
        RoleCommand.__init__(self, client, guild, role)

    def get_targets(self, roles):
        for guild in self.guild:
            roles_users_tuple = ([], [])
            if all_ in roles:
                roles_users_tuple[0].extend(guild.roles)
            else:
                for r in roles:
                    roles_users_tuple[0].append(guild.get_role(r))

            if self.target_users == all_:
                roles_users_tuple[1].extend(guild.members)
            else:
                for target in self.target_users:
                    member = guild.get_member(target)
                    if member is not None:
                        roles_users_tuple[1].append(member)
            if len(roles_users_tuple[0]) > 0 and len(roles_users_tuple[1]) > 0:
                self.role_user_list.append(roles_users_tuple)

    async def run(self):
        for role_user_tuple in self.role_user_list:
            for role in role_user_tuple[0]:
                for user in role_user_tuple[1]:
                    try:
                        await user.add_roles(role)
                        self.log_info(f"successfully gave {role} to {user}")
                    except Exception as e:
                        self.log_error(f"cannot gave {role} to {user}", error=e)
