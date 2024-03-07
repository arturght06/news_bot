import asyncio

from db.TGPostsUtils import TGPostsUtils
from db.AnalyzeProcessUtils import AnalyzeProcessUtils
from db.models import AnalyzeProcess, Post
# from TextAnalyzer.embedding_openai import


async def background_analyzer():
    analyzer_manager = AnalyzerMain()
    while True:
        await analyzer_manager.start_processes()
        await asyncio.sleep(5)


class AnalyzerMain:
    def __init__(self):
        self.posts_manager = TGPostsUtils()
        self.processes_manager = AnalyzeProcessUtils()

    async def start_processes(self):
        raw_posts = await self.posts_manager.get_with_filters()
        for post in iter(raw_posts):
            post_id = str(post.id)
            process: AnalyzeProcess = AnalyzeProcess(id=post_id)
            await self.processes_manager.set(process)
            new_processed_status: Post = Post(id=post_id, processed=True)
            await self.posts_manager.set(new_processed_status)

    # async def set_embeddings(self):



