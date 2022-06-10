from dataset import downloader


def test_get_false_func():
    downloader.download_file_from_google_drive("1IcSgVkp6Wh0vtGhFzdBELvm35cN6G46o", "test.zip")
    assert True
