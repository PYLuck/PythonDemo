# 人脸相似度比较:模型-人脸关键点检测器，人脸识别模型
"""
方法1:
 Ref: https://blog.csdn.net/m0_38106923/article/details/83862334; http://dlib.net/; https://pypi.org/simple/dlib/
 dlib库：C++工具箱，包含机器学习算法和工具；For Win系统: 新版Dlib库下载后需要在本地编译。编译要用到软件CMake，CMake编译CPP源代码还需要C++编译器。
    对于Windows系统，C++编译器在Visual Studio里面集成，所以需要安装Visual Studio并配置C++编译环境。
    python3.6环境: pip install dlib==19.7.0
方法2:百度API
Ref:https://blog.csdn.net/swan_tang/article/details/88769612

"""

import os, dlib, glob, numpy
from skimage import io

class FaceVsimilarity():

    def __init__(self, detector_path, face_rec_model_path, faces_folder_path, TestImg):
        # 人脸关键点检测器
        self.predictor_path = detector_path
        # 人脸识别模型、提取特征值
        self.face_rec_model_path = face_rec_model_path
        # 训练图像文件夹
        self.faces_folder_path = faces_folder_path

        # 测试数据
        self.TestImg = TestImg

    def run(self):
        # 加载模型
        detector = dlib.get_frontal_face_detector()
        sp = dlib.shape_predictor(self.predictor_path)
        facerec = dlib.face_recognition_model_v1(self.face_rec_model_path)

        candidate = []  # 存放训练集人物名字
        descriptors = []  # 存放训练集人物特征列表

        for f in glob.glob(os.path.join(self.faces_folder_path, "*.jpg")):
            print("正在处理: {}".format(f))
            img = io.imread(f)
            candidate.append(f.split('\\')[-1].split('.')[0])
            # 人脸检测
            dets = detector(img, 1)
            for k, d in enumerate(dets):
                shape = sp(img, d)
                # 提取特征
                face_descriptor = facerec.compute_face_descriptor(img, shape)
                v = numpy.array(face_descriptor)
                descriptors.append(v)

        print('计算他们的人脸特征，并放到一个列表里面:识别训练完毕！')

        try:
            # test_path=input('请输入要检测的图片的路径（记得加后缀哦）:')
            img = io.imread(self.TestImg)
            dets = detector(img, 1)
        except:
            print('输入路径有误，请检查！')

        dist = []
        global Range;   Range = 0  # 测试人脸与训练数据之间的欧式距离
        for k, d in enumerate(dets):
            shape = sp(img, d)
            face_descriptor = facerec.compute_face_descriptor(img, shape)
            d_test = numpy.array(face_descriptor)


            for i in descriptors:  # 计算距离
                dist_ = numpy.linalg.norm(i - d_test)
                dist.append(dist_)
                Range += dist_

        print("测试图与训练数据的平均相似度",1-(Range/len(dist)))

        # 训练集人物和距离组成一个字典
        c_d = dict(zip(candidate, dist))
        cd_sorted = sorted(c_d.items(), key=lambda d:d[1])

        print("识别到的相似度最高的人物:{} ,相似度为{}".format(cd_sorted[0][0], 1-cd_sorted[0][1]))
        print(cd_sorted)    # 距离值越小，相似度越高


# 方法2:腾讯
"""
class FaceVbaidu():
    import requests
    import base64
    import json
    # 1，准备好申请的人脸识别api，API Key， Secret Key
    api1 = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=Va5yQRHlA4Fq5eR30vV4&client_secret=0rDSjzQ20XUj5itV6WRtznPQSzr5pV"

    # api2="https://aip.baidubce.com/rest/2.0/face/v3/match"

    # 2,获取token值，拼接API
    def get_token():
        response = requests.get(api1)
        access_token = eval(response.text)['access_token']
        api2 = "https://aip.baidubce.com/rest/2.0/face/v3/match" + "?access_token=" + access_token
        return api2

    # 3,读取图片数据
    def read_img(img1, img2):
        with open(img1, 'rb') as f:
            pic1 = base64.b64encode(f.read())
        with open(img2, 'rb') as f:
            pic2 = base64.b64encode(f.read())
        params = json.dumps([
            {"image": str(pic1, "utf-8"), "image_type": 'BASE64', "face_type": "LIVE"},
            {"image": str(pic2, "utf-8"), "image_type": 'BASE64', "face_type": "IDCARD"}
        ])
        return params

    # 4，发起请求拿到对比结果
    def analyse_img(file1, file2):
        params = read_img(file1, file2)
        api = get_token()
        content = requests.post(api, params).text
        # print(content)
        score = eval(content)['result']['score']
        if score > 80:
            print('图片识别相似度度为' + str(score) + ',是同一人')
        else:
            print('图片识别相似度度为' + str(score) + ',不是同一人')

    analyse_img("zly01.jpg", "zly02.jpg")

    # 打印执行结果：图片识别相似度度为88.23068237,是同一人
    # 换图片zly02.jpg和lyf01.jpg：图片识别相似度度为29.28668785,不是同一人"""



if __name__ == '__main__':
    # 人脸关键点检测器
    detector_path = "G:\DeepLearn\DeepNet\Model_Saver\FaceRec\shape_predictor_68_face_landmarks.dat"
    # 人脸识别模型、提取特征值
    face_rec_model_path = "G:\DeepLearn\DeepNet\Model_Saver\FaceRec\dlib_face_recognition_resnet_model_v1.dat"
    # 训练图像文件夹
    faces_folder_path = "G:\DeepLearn\DeepNet\DataSet\FaceRecTrain"
    # 测试图片
    TestImg = "G:\DeepLearn\DeepNet\DataSet\FaceTest\my.jpg"

    Func = FaceVsimilarity(detector_path, face_rec_model_path, faces_folder_path, TestImg)
    Func.run()


















