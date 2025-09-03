from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from openai import OpenAI
import os
import json
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="工業高校生向け面接対策AI")

# 環境に応じたCORS設定
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

class ChatRequest(BaseModel):
    mode: str  # "employment" or "admission"
    message: str

class ChatResponse(BaseModel):
    reply: str

class QuickFeedbackRequest(BaseModel):
    mode: str
    question_num: int
    answer: str

class QuickFeedbackResponse(BaseModel):
    feedback: str

class Answer(BaseModel):
    question: str
    answer: str

class EvaluateRequest(BaseModel):
    mode: str
    answers: List[Answer]

class QuestionEvaluation(BaseModel):
    q: int
    score: float
    feedback: str
    detailed_analysis: str
    improvement_points: List[str]

class EvaluateResponse(BaseModel):
    summary_score: float
    questions: List[QuestionEvaluation]
    overall_feedback: str
    strengths: List[str]
    areas_for_improvement: List[str]
    next_steps: List[str]

# 就職面接向けシステムプロンプト
EMPLOYMENT_PROMPT = """
あなたは工業高校生の就職面接対策を支援する面接官AIです。

【役割】
- 製造業・技術職への就職を想定した面接指導
- 安全・品質・5S（整理・整頓・清掃・清潔・しつけ）を重視した回答の指導
- PREP法（Point結論→Reason理由→Example具体例→Point結論）を意識した構成指導

【指導方針】
1. まず学生の回答を評価し、良い点を1つ挙げる
2. 改善点を1-2点指摘し、具体的な改善案を提示
3. 技術職として重要な「安全意識」「品質意識」「チームワーク」「継続的な学習」を強調
4. PREP法やSTAR法（Situation状況→Task課題→Action行動→Result結果）での回答構成を推奨
5. 300文字以内で簡潔にフィードバック

工業高校生らしい具体的な体験談（実習、資格取得、部活動など）を盛り込むよう指導してください。
"""

ADMISSION_PROMPT = """
あなたは工業高校生の進学面接対策を支援する面接官AIです。

【役割】
- 大学・専門学校への進学を想定した面接指導
- 学修計画・研究関心・将来像を明確にする指導
- より高度な技術を学ぶ意欲と計画性を重視

【指導方針】
1. まず学生の回答を評価し、良い点を1つ挙げる
2. 改善点を1-2点指摘し、具体的な改善案を提示
3. 「なぜその分野を学びたいのか」「どのように学んでいくか」「将来どう活かすか」の明確化
4. 工業高校で学んだ基礎知識をどう発展させたいかを重視
5. PREP法やSTAR法での回答構成を推奨
6. 300文字以内で簡潔にフィードバック

高校での学習内容と進学先での学修内容の関連性を明確にするよう指導してください。
"""

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        if request.mode not in ["employment", "admission"]:
            raise HTTPException(status_code=400, detail="モードは 'employment' または 'admission' である必要があります")
        
        system_prompt = EMPLOYMENT_PROMPT if request.mode == "employment" else ADMISSION_PROMPT
        
        response = client.chat.completions.create(
            model=openai_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": request.message}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        reply = response.choices[0].message.content.strip()
        return ChatResponse(reply=reply)
        
    except Exception as e:
        error_msg = str(e)
        if "authentication" in error_msg.lower() or "api key" in error_msg.lower():
            raise HTTPException(status_code=401, detail="OpenAI APIキーが無効です")
        elif "rate limit" in error_msg.lower():
            raise HTTPException(status_code=429, detail="APIの利用制限に達しました")
        elif "openai" in error_msg.lower():
            raise HTTPException(status_code=500, detail=f"OpenAI API エラー: {str(e)}")
        else:
            raise HTTPException(status_code=500, detail=f"サーバーエラー: {str(e)}")

@app.post("/quick_feedback", response_model=QuickFeedbackResponse)
async def quick_feedback(request: QuickFeedbackRequest):
    """各質問の回答に対する簡単なフィードバック"""
    try:
        feedback_prompt = f"""
あなたは面接官です。工業高校生の回答に対して簡潔なフィードバックをしてください。

質問{request.question_num}: {get_question_text(request.question_num)}
回答: {request.answer}

以下の形式で50文字以内の簡潔なフィードバックを返してください：
- 良い点を1つ
- 改善提案を1つ（あれば）

回答例: "具体例が良いですね！もう少し数値を入れると更に説得力が増します。"
"""
        
        response = client.chat.completions.create(
            model=openai_model,
            messages=[{"role": "user", "content": feedback_prompt}],
            max_tokens=100,
            temperature=0.7
        )
        
        feedback = response.choices[0].message.content.strip()
        return QuickFeedbackResponse(feedback=feedback)
        
    except Exception as e:
        return QuickFeedbackResponse(feedback="ありがとうございます。次の質問に進みますね。")

@app.post("/evaluate", response_model=EvaluateResponse)
async def evaluate_interview(request: EvaluateRequest):
    """7つの質問すべての回答を5観点で評価"""
    try:
        evaluation_prompt = f"""
あなたは面接評価の専門家です。工業高校生の面接回答を以下の5観点で詳細に評価してください：

【評価観点】
1. 適合性（志望動機や価値観が適切か）
2. 論理構成（PREP法やSTAR法による構成）
3. 具体性（具体例や数値データの活用）
4. 表現力（話し方や伝える力）
5. マナー（敬語や面接態度）

【回答データ】
{format_answers_for_evaluation(request.answers)}

以下の形式のJSONを返してください：
{{
  "summary_score": 4.2,
  "questions": [
    {{
      "q": 1, 
      "score": 4.0, 
      "feedback": "具体例が豊富で説得力があります。",
      "detailed_analysis": "志望理由が明確で、会社の特色と自分の価値観の関連性を具体的に説明できている。特に安全への取り組みに言及した点は製造業への理解を示している。",
      "improvement_points": ["数値データを使った根拠の強化", "将来のキャリアビジョンをより具体的に"]
    }},
    ...
  ],
  "overall_feedback": "全体的に良い回答でした。特に...",
  "strengths": ["具体的な体験談の活用", "論理的な構成", "適切な敬語の使用"],
  "areas_for_improvement": ["数値データの活用不足", "STAR法の構成が不完全"],
  "next_steps": ["製造業の業界研究を深める", "数値を交えた実績の整理", "PREP法の練習を継続"]
}}

各質問について：
- score: 1.0〜5.0で評価
- feedback: 30文字程度の簡潔な総評
- detailed_analysis: 100文字程度の詳細分析（良い点と課題を具体的に）
- improvement_points: 具体的な改善提案を2-3個

全体について：
- strengths: 全体を通した強み3-5個
- areas_for_improvement: 改善が必要な分野2-4個
- next_steps: 具体的な次のアクション3-5個
"""
        
        response = client.chat.completions.create(
            model=openai_model,
            messages=[{"role": "user", "content": evaluation_prompt}],
            max_tokens=800,
            temperature=0.3
        )
        
        try:
            # JSONレスポンスをパース
            result = json.loads(response.choices[0].message.content.strip())
            
            return EvaluateResponse(
                summary_score=result["summary_score"],
                questions=[
                    QuestionEvaluation(
                        q=q["q"], 
                        score=q["score"], 
                        feedback=q["feedback"],
                        detailed_analysis=q.get("detailed_analysis", ""),
                        improvement_points=q.get("improvement_points", [])
                    )
                    for q in result["questions"]
                ],
                overall_feedback=result["overall_feedback"],
                strengths=result.get("strengths", []),
                areas_for_improvement=result.get("areas_for_improvement", []),
                next_steps=result.get("next_steps", [])
            )
        except json.JSONDecodeError:
            # JSONパースに失敗した場合のフォールバック
            return create_fallback_evaluation(request.answers)
            
    except Exception as e:
        return create_fallback_evaluation(request.answers)

def get_question_text(question_num: int) -> str:
    """質問番号から質問文を取得"""
    questions = [
        "志望した会社（または学校）を選んだ理由を具体的に教えてください。",
        "あなたの強みを1つ挙げて、それを示す具体的な経験を教えてください。",
        "チームやクラスで意見が分かれたとき、どのように行動しましたか？",
        "これまでに直面した一番大きな失敗と、それをどう乗り越えたかを教えてください。",
        "学校で学んだ専門知識や技術を、将来どのように活かしたいですか？",
        "働く（あるいは学ぶ）うえで大切にしたい価値観を教えてください。",
        "5年後、10年後にどのような人材になっていたいですか？"
    ]
    return questions[question_num - 1] if 1 <= question_num <= len(questions) else ""

def format_answers_for_evaluation(answers: List[Answer]) -> str:
    """評価用に回答をフォーマット"""
    formatted = []
    for i, answer in enumerate(answers, 1):
        formatted.append(f"質問{i}: {answer.question}\n回答{i}: {answer.answer}\n")
    return "\n".join(formatted)

def create_fallback_evaluation(answers: List[Answer]) -> EvaluateResponse:
    """エラー時のフォールバック評価"""
    questions = []
    for i in range(len(answers)):
        questions.append(QuestionEvaluation(
            q=i + 1,
            score=3.5,
            feedback="回答ありがとうございました。",
            detailed_analysis="面接練習への取り組み姿勢が評価できます。継続的な練習により更なる成長が期待できます。",
            improvement_points=["より具体的な事例の準備", "論理的な構成の練習"]
        ))
    
    return EvaluateResponse(
        summary_score=3.5,
        questions=questions,
        overall_feedback="面接練習お疲れさまでした。継続的な練習で更に向上できます。",
        strengths=["積極的な練習姿勢", "面接への真摯な取り組み"],
        areas_for_improvement=["具体的事例の充実", "論理構成の強化"],
        next_steps=["業界研究の深化", "自己分析の継続", "模擬面接の反復練習"]
    )

@app.get("/")
async def root():
    return {"message": "工業高校生向け面接対策AI"}

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    
    uvicorn.run(app, host=host, port=port, debug=debug)