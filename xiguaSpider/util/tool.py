import execjs
import js2py


def get_des_psswd():
    jsstr = get_js()
    # ctx = execjs.compile(jsstr) #加载JS文件
    # return (ctx.call('i'))  #调用js方法  第一个参数是JS的方法名，后面的data和key是js方法的参数
    data = js2py.eval_js(jsstr)
    print(data)
    return data


def get_js():
    f = open("./../util/param.js", 'r', encoding='utf-8')  # 打开JS文件
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
    return htmlstr


if __name__ == '__main__':
    get_des_psswd()
