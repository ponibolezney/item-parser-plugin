from .item_parser import parse_and_insert_item
import re

def setup(runner):
    @runner.on_message()
    async def handle_message(message, manager):
        user_input = message["human"]
        ai_response = message["bot"]

        loot_pattern = r'\[(.*?), \'(.*?)\', (.*?), (\d+)\]'
        matches = re.findall(loot_pattern, ai_response)

        for match in matches:
            item_type, name, description, damage = match
            parse_and_insert_item(f"!Добыча: [{item_type}, '{name}', {description}, {damage}]")

        await manager.send(ai_response)