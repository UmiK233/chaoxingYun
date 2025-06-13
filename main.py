import time

import requests

import os

# import urllib3
# urllib3.disable_warnings()


headers = {
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 14; 2210132C Build/UKQ1.230804.001) (schild:eb5855e665cb3a6db065e6d1c8a086be) (device:2210132C) Language/zh_CN com.chaoxing.mobile/ChaoXingStudy_3_6.5.9_android_phone_10890_281 (@Kalimdor)_0fe743fbc142436cab02bc393001f490",
    "Accept-Language": "zh_CN",
    "Connection": "Keep-Alive"
}

uid = "245326646"

cookies = {
    "_uid": uid,
    "_d": "1749708907724",
    "vc3": "SjqvSv5ztCkBffr0Oobuee5eAKlhbGyrCfQO079qhLsPxFIv2pAtpQbOxrGy1tkYR3s9oVFVJZ3WDclErYhhy0UMEMwwiBuPibquvabmC5swUCTiS7IWss9WdRFySuqkKiiq6A8ZnN9noJsw%2BNuCvZCH2TpgAvcREAvhfwpeie4%3D91dff97b6a49c2c8c00464e04cb1d0f9",
    "uf": "d9387224d3a6095b3f3e4a6e3cd3627f5cc0f9ef79f323b1f3026998d2a02f474b5b5a608bf16b65a69e3e1c4a1ee8d330d92481d752d66fab5213149d75dadbffcc3e0ecaa21d4f95aefb7b2721909126c48bfbbdfd645ca5f2f33c8c1f840245bc2cc8f3dac912dfd4860a93fcbeeafd2b9d97e810f79e92e069960b2e8dc8577a9aa095a87b2c",
}

get_token_url = "http://pan-yz.chaoxing.com/api/token/uservalid"

get_token_response = requests.get(url=get_token_url, cookies=cookies, headers=headers)

token = get_token_response.json()["_token"]


def get_files() -> list:
    get_files_url = f"http://pan-yz.chaoxing.com/api/getMyDirAndFiles?puid={uid}&fldid=&page=1&size=100&addrec=0&showCollect=1&_token={token}"

    # 发送GET请求
    get_files_response = requests.get(url=get_files_url, headers=headers, cookies=cookies)

    files_list = get_files_response.json()["data"]
    # print(files_list)
    for i, e in enumerate(files_list):
        print(f"文件{i}:{e['name']} resid:{e['resid']} encryptedId:{e['encryptedId']} size:{e['size']}")
    return files_list


def download(file_dict:dict, file_name=None):
    """ 下载文件
    :param file_dict: 文件字典
    :param file_name: 下载的文件名,可选
    {'disableOpt': False, 'resid': 1140377977306210304, 'encryptedId': '6b6c599590216fa94662605118d0cda5ec64ec185782ce63', 'crc': '115fae6db495b99092f2f248cfbac6e4', 'puid': 245326646, 'isfile': True, 'pantype': 'USER_PAN', 'size': 12523, 'name': 'adwadadwada.txt', 'objectId': '87c53612c3a4b292e42f01c72f47f05c', 'restype': 'RES_TYPE_YUNPAN_FILE', 'uploadDate': 1749816897000, 'modifyDate': 1749816897000, 'uploadDateFormat': '2025-06-13', 'residstr': '1140377977306210304', 'suffix': 'txt', 'preview': 'http://pan-yz.chaoxing.com/preview/showpreview_1140377977306210304.html?v=1749817146026&enc=37571ad8d81c4641e27f831f80773ba0', 'thumbnail': '', 'creator': 245326646, 'duration': 0, 'isImg': False, 'isOffice': False, 'isMirror': False, 'filetype': '', 'filepath': '', 'sort': 101, 'topsort': 0, 'resTypeValue': 1, 'extinfo': ''}
    :return: 下载是否成功 True/False
    """
    if file_name is None:
        file_name = file_dict["name"]
    # file_size = file_dict["size"]
    res_id = file_dict["resid"]
    get_download_url = f"http://pan-yz.chaoxing.com/api/getDownloadUrl?puid={uid}&fleid={res_id}&_token={token}"

    # 获取下载直链
    get_download_response = requests.get(url=get_download_url, headers=headers, cookies=cookies)
    print(get_download_response.json())

    download_url = get_download_response.json()["url"]
    download_headers = {
        # 使用手机UA也可以下载不被拒绝访问
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 14; 2210132C Build/UKQ1.230804.001) (schild:eb5855e665cb3a6db065e6d1c8a086be) (device:2210132C) Language/zh_CN com.chaoxing.mobile/ChaoXingStudy_3_6.5.9_android_phone_10890_281 (@Kalimdor)_0fe743fbc142436cab02bc393001f490",
        # "Range": f"bytes=0-{file_size}",
        "Accept-Language": "zh_CN",
        "Referer": download_url,  # 关键参数,否则会被拒绝访问
        "Connection": "Keep-Alive"
    }
    download_response = requests.get(url=download_url, headers=download_headers, cookies=cookies)

    with open(file_name, "wb") as f:
        f.write(download_response.content)
    if download_response.status_code == 200:
        return True
    else:
        print(download_response.text)
        return False


def delete_file(resid):
    """ 删除文件
    :param resid: 文件的id
    :return:删除操作的结果 True/False
    """
    delete_url = f"http://pan-yz.chaoxing.com/api/delete?puid={uid}&resids={resid}&_token={token}"
    delete_response = requests.get(url=delete_url, headers=headers, cookies=cookies)
    result = delete_response.json()["result"]
    print(delete_response.text)
    return result


def upload_files(file_path, file_name=None):
    """ 上传文件
    :param file_path: 上传的文件路径,建议绝对路径,相对路径时需注意执行位置
    :param file_name: 上传到云盘中的文件名,可选,默认从文件路径中解析
    :return:返回上传结果 True/False
    """
    if file_name is None:
        file_name = os.path.basename(file_path)
    # print(file_name)
    files = [
        ('file', (file_name, open(file_path, 'rb'), "application/octet-stream"))
    ]
    upload_url = f"http://pan-yz.cldisk.com/upload/uploadfile?_token={token}&puid={uid}"
    upload_response = requests.post(url=upload_url, headers=headers, files=files)
    # {'code': -6, 'msg': '不能识别的文件类型, 上传失败', 'newCode': 200009, 'result': False}
    print(upload_response.json())
    if upload_response.json()["result"] == False:
        print(upload_response.json()["newCode"])
        if upload_response.json()["newCode"] == 200009:
            # 先上传一个正常文件
            modified_file_name = os.path.splitext(file_name)[0] + ".txt"
            modified_files = [
                ('file', (modified_file_name, open(file_path, 'rb'), "application/octet-stream"))
            ]
            modified_upload_response = requests.post(url=upload_url, headers=headers, files=modified_files)
            print(modified_upload_response.json())
            # 获取他的crc校验码
            crc = modified_upload_response.json()["data"]["crc"]
            file_size = modified_upload_response.json()["data"]["size"]
            # 把上传的替身文件删除
            delete_file(modified_upload_response.json()["data"])

            newfile_url = f"https://pan-yz.chaoxing.com/api/newfle?_token={token}"
            newfile_data = {
                "puid": uid,
                "fs": file_size,  # 文件大小
                "fndest": file_name,  # 也是文件名,但是并不决定上传后的文件名称
                "fnorigin": file_name,  # 文件名
                "date": str(int(time.time() * 1000)),
                "crc": crc,
                # "fldid": "0"
            }
            newfile_response = requests.post(url=newfile_url, headers=headers, data=newfile_data)
            print(newfile_response.json())

            return modified_upload_response.json()["result"]

    return upload_response.json()["result"]


# upload_files("./files.json")
# download()
get_files()
download(get_files()[1],"files.json")
# delete_file(get_files()[0]["resid"])
