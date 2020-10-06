from advanced_decline_checker.ratio_service import RatioService
from advanced_decline_checker.message_service import MessageService


def check_ratio() -> bool:
    try:
        advancec_decline_ratio = RatioService().get_today_ratio()
        if advancec_decline_ratio is not None:
            message = advancec_decline_ratio.generate_message()
            MessageService(message).post()
        return True
    except Exception as e:
        print(e)
        return False


if __name__ == '__main__':
    advancec_decline_ratio = RatioService().get_today_ratio()
    print(advancec_decline_ratio.generate_message())
