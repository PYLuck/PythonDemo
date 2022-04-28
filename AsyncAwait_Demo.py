"""协程的语法糖 async和await: 适用python3.5之后的版本
async def 用来定义异步函数，await 表示当前协程任务等待睡眠时间，允许其他任务运行。
然后获得一个事件循环，主线程调用asyncio.get_event_loop()时会创建事件循环，
你需要把异步的任务丢给这个循环的run_until_complete()方法，事件循环会安排协同程序的执行
"""
import time
import asyncio

# 定义异步函数
async def hello():
    # 在协程函数中，可以通过await语法来挂起自身的协程，并等待另一个协程完成直到返回结果
    await asyncio.sleep(1)
    print('Hello World:%s' % time.time())
# 直接调用异步函数不会返回结果，而是返回一个coroutine对象


if __name__ == '__main__':
    # 主线程——创建事件循环
    loop = asyncio.get_event_loop()
    tasks = [hello() for i in range(5)]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()