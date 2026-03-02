from youtube_transcript_api import YouTubeTranscriptApi


def get_transcript(videoID):
    transcript_list = YouTubeTranscriptApi().fetch(
        videoID,
        languages=["hi", "en"]
    )
    text = " ".join(chunk.text for chunk in transcript_list.snippets)
    return text


def format_docs(retrieved_docs):
    return "\n\n".join(doc.page_content for doc in retrieved_docs)