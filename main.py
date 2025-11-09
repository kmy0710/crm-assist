"""
메인 애플리케이션 진입점
CRM 기반 디바이스 마케팅 자동화의 전체 흐름을 제어합니다.
"""
import sys
from config import Config
from api.openai_api import OpenAIClient
from api.qlik_api import QlikClient
from agent.crm_recommend import CRMRecommendationEngine
from agent.crm_image_generator import CRMImageGenerator

def main():
    """메인 함수"""
    # 설정 로드
    config = Config()
    
    # 설정 검증
    if not config.validate():
        print("오류: 필수 설정값이 누락되었습니다.")
        print("다음 환경 변수를 설정해주세요:")
        print("- OPENAI_API_KEY")
        print("- QLIK_SERVER")
        print("- QLIK_APP_ID")
        print("- CRM_API_URL")
        sys.exit(1)
    
    # 클라이언트 초기화
    openai_client = OpenAIClient(config)
    qlik_client = QlikClient(config)
    
    # CRM 이미지 및 고객 추천 엔진 초기화
    image_generator = CRMImageGenerator(config)
    recommendation_engine = CRMRecommendationEngine(openai_client, qlik_client)
    
    # 이미지 생성 예시
    print("\nCRM 캠페인 이미지 생성 예시를 실행합니다...")
    prompt = (
        "High-resolution marketing poster for premium 5G smartphone bundle, "
        "featuring sleek futuristic design, vibrant blue and silver color scheme, "
        "dynamic lighting, text placeholder for headline and CTA, professional studio background"
    )

    try:
        image_generator.generate_campaign_images(prompt)

    except Exception as exc:
        print(f"이미지 생성 중 오류가 발생했습니다: {exc}")

if __name__ == "__main__":
    main()

