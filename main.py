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
    
    # CRM 추천 엔진 초기화
    recommendation_engine = CRMRecommendationEngine(openai_client, qlik_client)
    image_generator = CRMImageGenerator(config)
    
    # 예시: 고객 ID로 디바이스 추천
    customer_id = "CUSTOMER_001"
    
    print(f"고객 {customer_id}에 대한 디바이스 추천을 시작합니다...")
    
    result = recommendation_engine.recommend_devices_for_customer(customer_id)
    
    if result:
        print("\n=== 추천 결과 ===")
        print(f"고객 ID: {result['customer_id']}")
        print(f"\n추천 디바이스 ({len(result['recommendations'])}개):")
        
        for idx, rec in enumerate(result['recommendations'], 1):
            print(f"\n{idx}. {rec['device_name']} (ID: {rec['device_id']})")
            print(f"   점수: {rec['score']:.2f}")
            print(f"   추천 이유: {rec['recommendation']}")
    else:
        print("추천 결과를 생성할 수 없습니다.")

    # 이미지 생성 예시
    print("\nCRM 캠페인 이미지 생성 예시를 실행합니다...")
    prompt = (
        "High-resolution marketing poster for premium 5G smartphone bundle, "
        "featuring sleek futuristic design, vibrant blue and silver color scheme, "
        "dynamic lighting, text placeholder for headline and CTA, professional studio background"
    )

    try:
        images = image_generator.generate_campaign_images(
            prompt,
            negative_prompt="low resolution, blurry, watermark",
            size="1024x1024",
            count=1,
        )

        if images:
            print("이미지 생성 성공! 반환된 데이터 요약:")
            first = images[0]
            if "url" in first:
                print(f"- 이미지 URL: {first['url']}")
            elif "b64_json" in first:
                print(f"- base64 문자열 길이: {len(first['b64_json'])}")
            else:
                print(f"- 기타 응답 필드: {list(first.keys())}")
        else:
            print("이미지 응답 데이터가 비어 있습니다.")
    except Exception as exc:
        print(f"이미지 생성 중 오류가 발생했습니다: {exc}")


if __name__ == "__main__":
    main()

