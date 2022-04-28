"""Python设计模型——面向对象:   封装->继承->多态(Python本身是一门多态语言)
设计原则: SOLID原则
接口:若干抽象方法的集合
"""
# -*- coding:utf-8 -*-
# 如何定义接口 —— 1.接口隔离原则（使用多个专门的接口，而不使用单一的总接口）;
    #           2.单一职责原则 一个类只负责一项职责
# 接口的作用：1.限制 继承该接口(Payment)的Alipay 必须 也实现一个同样的pay()方法;
        #   2.对高层模块(PP)隐藏了类Alipay的内部实现

from abc import ABCMeta,abstractmethod

# 工厂模式
class Payment(metaclass=ABCMeta):   # 抽象产品
    # 抽象类
    @abstractmethod
    def pay(self,money):
        print('支付')

# 接口
class Alipay(Payment):      # 具体产品
    def __init__(self, huabei=False):
        self.huabei = huabei

    def pay(self, money):
        if self.huabei:
            print('花呗支付')
        else:
            print('支付宝支付')

class WechatPay(Payment):
    def pay(self,money):
        print('微信支付')

PP = Alipay().pay(100)

# 建造者模式-----------------------------------------------------------

class PlayerBuilder(metaclass=ABCMeta):     # 抽象接口
    @abstractmethod
    def build_face(self):
        pass

    @abstractmethod
    def build_body(self):
        pass

    @abstractmethod
    def build_arm(self):
        pass

    @abstractmethod
    def build_leg(self):
        pass

class Player:       # 属性
    def __init__(self, face=None, body=None, arm=None, leg=None):
        self.face = face
        self.body = body
        self.arm = arm
        self.leg = leg

    def __str__(self):
        return "%s, %sm, %s , %s" % (self.face, self.body, self.arm, self.leg)

# 具体实例
class SexyGirlBuilder(PlayerBuilder):
    def __init__(self):
        self.player = Player()

    def build_face(self):
        self.player.face = "漂亮脸蛋"

    def build_body(self):
        self.player.body = "苗条"

    def build_arm(self):
        self.player.arm = "漂亮胳臂"

    def build_leg(self):
        self.player.leg = "长腿"




if __name__ == '__main__':
    '''
    设计模式分类:
    创建型模式（5'）:工厂方法,抽象工厂,创建者,原型,单例模式
    结构型模式（7'）:适配器,桥,组合,装饰,外观,享元,代理模式
    行为型模式（11'）:解释器,责任链,命令,迭代器,中介,备忘录,观察者,状态,策略,\
                    访问者,模板方法模式
    '''

# ======================创建型模型============================================== #

    '''创建模式'''
    # 简单工厂模式: 通过工厂类创建产品类的实例
    class PaymentFactory:       # 创建者
        def create_payment(self,method):
            if method == "alipay":
                return Alipay()
            elif method == "wechat":
                return WechatPay()
            elif method == "huabei":
                return Alipay(huabei=True)
            else:
                return TypeError("No such payment named %s" % method)

    # client
    pf = PaymentFactory().create_payment("huabei")
    pf.pay(100)


    # 工厂方法模式——定义一个工厂接口(抽象工厂)
    class BankPay(Payment):     # 新增具体产品
        def pay(self,money):
            print('银联支付')

    class Paymentfactory(metaclass=ABCMeta):       # 创建者
        @abstractmethod
        def create_payment(self):
            pass

    # 抽象工厂子类(每一个子类也可实现一系列方法)
    class AlipayFactory(PaymentFactory):
        def create_payment(self,**kwargs):
            return Alipay()
    class WechatFactory(PaymentFactory):
        def create_payment(self,**kwargs):
            return WechatPay()
    class HuabeiFactory(PaymentFactory):
        def create_payment(self,**kwargs):
            return Alipay(huabei=True)
    class BankPayFactory(Paymentfactory):
        def create_payment(self):
            return BankPay()
    # client
    pfc = BankPayFactory().create_payment()
    pfc.pay(100)



    '''建造者模型: 建造者可以创建不同表示'''
# ———————————抽象建造者, 具体建造者, 指挥者,产品——————————————

    # 指挥者：指挥建造 顺序
    class PlayerDirector:
        def build_player(self,builder):     # 控制组装顺序
            builder.build_body()
            builder.build_face()
            builder.build_arm()
            builder.build_leg()
            return builder.player

    # client
    builder = SexyGirlBuilder()
    director = PlayerDirector()
    P = director.build_player(builder);    print(P)

    '''单例模式:保证一个类只有一个实例，并提供一个访问它的全局访问点'''
    class Singleton:
        def __new__(cls, *args, **kwargs):
            # 判断类对象(cls)是否包含对应的属性(_instance)
            if not hasattr(cls, "_instance"):
                cls._instance = super(Singleton, cls).__new__(cls)
            return cls._instance

    class MyClass(Singleton):
        def __init__(self,a):
            self.a = a
    a = MyClass(10)
    b = MyClass(20)
    print(a.a, b.a, id(a) == id(b))     # a,b是一样的，只有一个实例Myclass()


# ==================结构型模式==================================================== #

    '''适配器模式:
    适用场景: 想用一个已存在的类，而它的接口不符合你的要求'''
    class BankPay2:
        def cost(self, money):
            print("新银联2支付%d元." % money)

    # 类适配器:通过继承BankPay2, 将本来不兼容的cost, 与原来的pay兼容
    class NewBankPay(Payment, BankPay2):
        def pay(self,money):
            self.cost(money)

    # 对象适配器:传入类对象的方式
    class PaymentAdapter(Payment):
        def __init__(self, Payment):
            self.payment = Payment      # 这里不需要实例化(),传的只是接口对象Payment
        def pay(self,money):
            self.payment.cost(money)

    P2 = PaymentAdapter(BankPay2())
    P2.pay(100)

    '''桥模式
    将一个事物的2个维度分离，使其都可以独立变化
    '''
    # 松耦合: 形状接口,颜色接口;   使颜色和形状都可以扩展
    class Shape(metaclass=ABCMeta):
        def __init__(self,color):
            self.color = color
        @abstractmethod
        def draw(self):
            pass
    class Color(metaclass=ABCMeta):
        @abstractmethod
        def paint(self,shape):
            pass

    # 抽象 一个方形
    class Rectangle(Shape):
        name = "长方形"
        def draw(self):
            self.color.paint(self)      # 调用红色画笔
    # 实现 红色的笔
    class RedPen(Color):
        def paint(self,shape):
            print("红色的%s" % shape.name)
    # 高层代码
    Rectangle(RedPen()).draw()


    '''组合模式'''
    # 抽象组件
    class Graphic(metaclass=ABCMeta):
        @abstractmethod
        def draw(self):
            pass

    # 叶子组件
    class Point(Graphic):
        def __init__(self,x,y):
            self.x = x
            self.y = y
        def __str__(self):
            return "点(%s, %s)" %(self.x, self.y)
        def draw(self):
            print(str(self))
    class Line(Graphic):
        def __init__(self, p1, p2):
            self.p1 = p1
            self.p2 = p2
        def __str__(self):
            return "线段[%s, %s]" % (self.p1, self.p2)
        def draw(self):
            print(str(self))

    # 复合组件
    class Picture(Graphic):
        def __init__(self,iterable):
            self.children = []
            for g in iterable:
                self.add(g)
        def add(self,graphic):
            self.children.append(graphic)
        def draw(self):
            print("--复合图像--")
            for g in self.children:
                g.draw()
            print("--复合图像————")

    # 部分
    l1 = Line(Point(1,2),Point(3,3))
    l2 = Line(Point(4,5),Point(6,6))
    # 组合（整体）
    Picture([l1, l2]).draw()

    '''外观模式'''
    # 子系统类
    class CPU:
        def run(self):
            print("CPU 开始运行")
        def stop(self):
            print("CPU停止运行")
    class Disk:
        def run(self):
            print("硬盘 开始运行")
        def stop(self):
            print("硬盘停止运行")
    class Memory:
        def run(self):
            print("内存 通电")
        def stop(self):
            print("内存断电")
    # 外观
    class Computer:
        def __init__(self):
            self.cpu = CPU()
            self.disk = Disk()
            self.memory = Memory()
        def run(self):
            self.cpu.run()
            self.disk.run()
            self.memory.run()
        def stop(self):
            self.cpu.stop()
            self.disk.stop()
            self.memory.stop()

    # client
    computer = Computer()
    computer.run()
    computer.stop()

    '''代理模型
    应用场景: 
    远程代理: 为远程对象提供代理;
    虚代理: 根据需要 创建很大的对象;
    保护代理: 控制对原始对象的访问，用于对象有不同的访问权限
    '''
    class Subject(metaclass=ABCMeta):
        @abstractmethod
        def get_content(self):
            pass
        @abstractmethod
        def set_content(self, content):
            pass

    class RealSubject(Subject):
        def __init__(self, filename):
            self.filename = filename
            f = open(filename,'r',encoding='utf-8')
            self.content = f.read()
            f.close()
        def get_content(self):
            return self.content
        def set_content(self, content):
            f = open(self.filename,'w',encoding='utf-8')
            f.write(content)
            f.close()

    # 根据需要读取-创建对象
    class VirtualProxy(Subject):
        def __init__(self,filename):
            self.filename = filename
            self.subj = None
        def get_content(self):
            if not self.subj:
                self.subj = RealSubject(self.filename)
            return self.subj.get_content()
        def set_content(self, content):
            if not self.subj:
                self.subj.set_content(self.filename)
            return self.subj.set_content(content)


# ==================行为型模式==================================================== #
    '''观察者模式(发布-订阅模式)'''
    class Observer(metaclass=ABCMeta):      # 抽象的订阅者
        @abstractmethod
        def update(self, notice):       # notice 是一个Notice类
            pass

    class Notice:       # 抽象的发布者
        def __init__(self):
            self.observer = []

        def attach(self,obs):
            self.observer.append(obs)

        def deattch(self,obs):
            self.observer.remove(obs)

        def notify(self):       # 推送
            for obs in self.observer:
                obs.update(self)

    class StaffNotice(Notice):      # 具体的发布者
        def __init__(self, company_info=None):
            super(StaffNotice, self).__init__()
            self.__company_info = company_info

        @property
        def company_info(self):
            return self.__company_info

        @company_info.setter
        def company_info(self,info):
            self.__company_info = info     # 1.发布（赋值）内容
            self.notify()       # 2.自动推送 -> 已attach的用户

            
    class Staff(Observer):
        def __init__(self):
            self.company_info = None
        def update(self, notice):
            self.company_info = notice.company_info

    # client
    notice = StaffNotice('初始化公司信息')
    s1 = Staff()
    s2 = Staff()
    notice.attach(s1)
    notice.attach(s2)
    # 发布具体内容
    notice.company_info = "本公司业绩报表已推送"
    # 只要s1和s2绑定好,
    # 一旦有内容发布(赋值)，会自动接到推送
    print(s1.company_info, '\n',s2.company_info)
    notice.deattch(s2)
    notice.company_info = '通知:s2业绩垫底,公司已将s2开除'
    print(s1.company_info, '\n', s2.company_info)

# -----------------------------------------
    '''策略模型:定义一系列策略算法，把他们一个个封装起来，并使他们可相互替换 '''
    # 抽象策略,具体策略,上下文
    class Context:
        def __init__(self,stragety,data):
            self.data = data
            self.stragety = stragety

        def set_stragety(self,stragety):    # 调度策略
            self.stragety = stragety
        def do_stragety(self):
            self.stragety.zhixing(self.data)    # 执行策略



# --------------------------------------------
    '''模板方法模式'''
    class Window(metaclass=ABCMeta):
        @abstractmethod
        def start(self):
            pass

        @abstractmethod
        def repaint(self):
            pass

        @abstractmethod
        def close(self):
            pass

        def run(self):      # 模板方法
            from time import sleep
            self.start()
            while True:
                try:
                    self.repaint()
                    sleep(1)
                except KeyboardInterrupt:
                    break
            self.close()

    class MyWindow(Window):
        def __init__(self,msg):
            self.msg = msg

        def start(self):
            print("窗口开始运行")

        def repaint(self):
            print(self.msg)

        def close(self):
            print("窗口结束运行")

        def run(self):
            from time import sleep
            self.start()
            while True:
                try:
                    self.repaint()
                    sleep(1)
                except KeyboardInterrupt:
                    break
            self.close()

    # clent
    MyWindow("Hello").run()







