import parser
from main import client, server_ip


def test_iperf_client_pass():
    """Тест проходить: сервер активний, помилки немає, показники вище порогу."""
    stdout, error = client(server_ip)
    assert error == "", f"Очікувалась відсутність помилки, отримано: {error}"

    intervals = parser.parser(stdout)
    assert len(intervals) > 0, "Не знайдено жодного інтервалу"

    for item in intervals:
        assert item["Transfer"] > 2, f"Замалий Transfer: {item}"
        assert item["Bitrate"] > 20, f"Замалий Bitrate: {item}"


def test_iperf_high_threshold_fail():
    """Тест не проходить: поріг пропускної здатності завищений (наприклад, > 100000 Мбіт/с)."""
    stdout, error = client(server_ip)
    assert error == ""

    intervals = parser.parser(stdout)
    for item in intervals:
        assert item["Bitrate"] > 100000, (
            f"Bitrate ({item['Bitrate']}) не перевищує очікуваний поріг 100000"
        )