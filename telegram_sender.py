from os import environ as env
import asyncio
from qusasat import Qusasat
import telegram
import dotenv

class MyBot(telegram.Bot):
    def __init__(
            self, token: str, chat_id: str, messages_signature: str = ""):
        super().__init__(token=token)
        self._chat_id = chat_id
        self._messages_signature = messages_signature
    
    async def send_post(self, post: dict):
        return await self.send_message(
            chat_id=self._chat_id,
            text=f"<blockquote>{post['quote']}</blockquote>\n\n<b>({post['category']})</b>\n\n{self._messages_signature}",
            parse_mode='HTML',
        )

def run():
    dotenv.load_dotenv()
    token = env.get("TELEGRAM_BOT_TOKEN")
    chat_id = env.get("TELEGRAM_CHAT_ID")
    messages_signature = env.get("MESSAGES_SIGNATURE")
    bot = MyBot(
        token=token, chat_id=chat_id, messages_signature=messages_signature)
    asyncio.run(bot_run(bot=bot))

async def bot_run(bot: MyBot):
    qusasat = Qusasat(
        categories_file='./data/categories.csv',
        quotes_file='./data/qusasat.csv'
    )
    random_post = qusasat.get_random_quote()
    async with bot:
        await bot.send_post(random_post)

if __name__ == '__main__':
    run()
