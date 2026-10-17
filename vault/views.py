from django.db.models.functions import Random
from django.http import HttpResponse, HttpResponseRedirect
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import JokeStore
from .serializers import JokeStoreSerializer


@csrf_exempt
def index(request):
    if request.method == 'POST':
        story_text = request.POST.get('story')
        if story_text and story_text.strip():
            JokeStore.objects.create(text=story_text.strip())
        return HttpResponseRedirect('/')

    random_story = JokeStore.objects.order_by(Random()).first()

    story_id = random_story.id if random_story else 'null'
    story_text = (
        random_story.text
        if random_story
        else 'The vault is currently empty. Be the first to publish a story!'
    )
    story_likes = random_story.likes if random_story else 0

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JokeStore — Developer Humor Vault</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-page: #0f172a;
            --bg-card: rgba(30, 41, 59, 0.75);
            --border-card: rgba(255, 255, 255, 0.12);
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --accent-pink: #ec4899;
            --accent-purple: #8b5cf6;
            --accent-indigo: #6366f1;
        }}

        * {{ box-sizing: border-box; margin: 0; padding: 0; }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--bg-page);
            background-image: 
                radial-gradient(at 0% 0%, rgba(236, 72, 153, 0.12) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(99, 102, 241, 0.15) 0px, transparent 50%);
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 24px;
        }}

        .container {{
            width: 100%;
            max-width: 580px;
        }}

        .header {{
            text-align: center;
            margin-bottom: 28px;
        }}

        .header h1 {{
            font-size: 2.25rem;
            font-weight: 700;
            background: linear-gradient(135deg, #f472b6, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 6px;
            letter-spacing: -0.02em;
        }}

        .header p {{
            color: var(--text-secondary);
            font-size: 0.95rem;
        }}

        .card {{
            background: var(--bg-card);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--border-card);
            border-radius: 20px;
            padding: 28px;
            box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.5);
            margin-bottom: 20px;
        }}

        .card-title {{
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #a78bfa;
            margin-bottom: 14px;
        }}

        .joke-text {{
            font-size: 1.15rem;
            font-weight: 500;
            line-height: 1.6;
            color: var(--text-primary);
            margin-bottom: 24px;
            background: rgba(15, 23, 42, 0.5);
            padding: 16px;
            border-radius: 12px;
            border-left: 4px solid var(--accent-pink);
        }}

        .action-row {{
            display: flex;
            gap: 10px;
        }}

        .btn {{
            font-family: inherit;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            padding: 10px 18px;
            border-radius: 12px;
            font-size: 0.875rem;
            font-weight: 600;
            cursor: pointer;
            border: 1px solid transparent;
            transition: all 0.2s ease;
        }}

        .btn-like {{
            background: rgba(236, 72, 153, 0.1);
            border-color: rgba(236, 72, 153, 0.3);
            color: #f472b6;
            flex: 1;
        }}

        .btn-like:hover:not(:disabled) {{
            background: rgba(236, 72, 153, 0.2);
            transform: translateY(-1px);
        }}

        .btn-like:disabled {{
            opacity: 0.6;
            cursor: not-allowed;
            background: rgba(255, 255, 255, 0.05);
            border-color: var(--border-card);
            color: var(--text-secondary);
        }}

        .btn-secondary {{
            background: rgba(255, 255, 255, 0.05);
            border-color: var(--border-card);
            color: var(--text-primary);
            text-decoration: none;
        }}

        .btn-secondary:hover {{
            background: rgba(255, 255, 255, 0.1);
            transform: translateY(-1px);
        }}

        .btn-primary {{
            background: linear-gradient(135deg, var(--accent-purple), var(--accent-indigo));
            color: #ffffff;
            width: 100%;
            padding: 12px;
            font-size: 0.95rem;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
        }}

        .btn-primary:hover {{
            opacity: 0.95;
            transform: translateY(-1px);
        }}

        .form-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: 20px;
            padding: 24px;
        }}

        .form-card h3 {{
            font-size: 1rem;
            margin-bottom: 14px;
            color: var(--text-primary);
        }}

        textarea {{
            width: 100%;
            font-family: inherit;
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid var(--border-card);
            border-radius: 12px;
            padding: 12px;
            color: var(--text-primary);
            font-size: 0.95rem;
            outline: none;
            resize: vertical;
            min-height: 70px;
            margin-bottom: 14px;
            transition: border-color 0.2s ease;
        }}

        textarea:focus {{
            border-color: var(--accent-purple);
        }}

        .footer-nav {{
            margin-top: 20px;
            text-align: center;
        }}

        .footer-nav a {{
            color: var(--text-secondary);
            text-decoration: none;
            font-size: 0.85rem;
            font-weight: 500;
            transition: color 0.2s ease;
        }}

        .footer-nav a:hover {{
            color: #a78bfa;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🙈 JokeStore Vault</h1>
            <p>Anonymized developer confessions & jokes collection</p>
        </div>

        <!-- Joke Card -->
        <div class="card">
            <div class="card-title">🎲 Random Entry</div>
            <div class="joke-text" id="storyText">“{story_text}”</div>
            <div class="action-row">
                <button class="btn btn-like" id="likeBtn" onclick="likeCurrentStory()">
                    ❤️ Like (<span id="likeCount">{story_likes}</span>)
                </button>
                <button class="btn btn-secondary" onclick="window.location.reload()">
                    🔄 Next Entry
                </button>
            </div>
        </div>

        <!-- Add Form -->
        <div class="form-card">
            <h3>📝 Publish a New Entry</h3>
            <form method="POST">
                <textarea name="story" placeholder="Share a story or joke anonymously..." required></textarea>
                <button type="submit" class="btn btn-primary">Publish to Vault</button>
            </form>
        </div>

        <div class="footer-nav">
            <a href="/swagger/" target="_blank">📖 Swagger OpenAPI Specification</a>
        </div>
    </div>

    <script>
        let currentStoryId = {story_id};

        async function likeCurrentStory() {{
            if (!currentStoryId) return;

            const btn = document.getElementById('likeBtn');
            const likeCountElem = document.getElementById('likeCount');

            // Disable button immediately to prevent multi-clicking
            btn.disabled = true;

            try {{
                const res = await fetch(`/api/story/${{currentStoryId}}/rank/`, {{
                    method: 'PUT'
                }});

                if (res.ok) {{
                    const data = await res.json();
                    likeCountElem.innerText = data.likes;
                    btn.innerHTML = `💖 Liked (${{data.likes}})`;
                }} else {{
                    btn.disabled = false;
                }}
            }} catch (err) {{
                console.error("Error liking story:", err);
                btn.disabled = false;
            }}
        }}
    </script>
</body>
</html>"""
    return HttpResponse(html_content)


class RandomStoryAPIView(APIView):

    @extend_schema(
        summary='Get random joke', responses={200: JokeStoreSerializer, 404: dict}
    )
    def get(self, request):
        story = JokeStore.objects.order_by(Random()).first()
        if not story:
            return Response(
                {'detail': 'No jokes yet'}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = JokeStoreSerializer(story)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateStoryAPIView(APIView):

    @extend_schema(
        summary='Post a joke',
        request=JokeStoreSerializer,
        responses={201: JokeStoreSerializer, 400: dict},
    )
    def post(self, request):
        serializer = JokeStoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class RankStoryAPIView(APIView):
    @extend_schema(
        summary="Like a joke by ID (PUT)",
        responses={200: JokeStoreSerializer, 404: dict},
    )
    def put(self, request, pk):
        story = get_object_or_404(JokeStore, pk=pk)
        story.likes += 1
        story.save()
        serializer = JokeStoreSerializer(story)
        return Response(serializer.data, status=status.HTTP_200_OK)
