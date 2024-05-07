from aiogram.dispatcher.filters import Filter
from aiogram.types import Message
from data.config import admin_ids
class IsAdminFilter(Filter):
    async def check(self, message: Message) -> bool:
        # Your logic to determine if the user is an admin
        # For example, you can check if the user's ID is in a list of admin IDs
        return message.from_user.id in admin_ids  # Replace [1, 2, 3] with actual admin IDs

# Usage:
