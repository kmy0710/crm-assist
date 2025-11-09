"""
메인 애플리케이션 진입점
CRM 기반 디바이스 마케팅 자동화의 전체 흐름을 제어합니다.
"""
import sys
from config import Config
from openai_api import OpenAIClient
from qlik_api import QlikClient
from crm_recommend import CRMRecommendationEngine

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
    
    # 예시: 고객 ID로 디바이스 추천
    # 실제 사용 시에는 명령줄 인자나 API에서 받아올 수 있습니다
    customer_id = "CUSTOMER_001"  # 실제 고객 ID로 변경 필요
    
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


if __name__ == "__main__":
    main()

