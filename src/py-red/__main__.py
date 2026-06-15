import STPyV8

class Console(object):
    def log(self, message):
        print(message)

    def error(self, message):
        print(message)

class Global(STPyV8.JSClass):
    # per https://nodejs.org/api/modules.html
    cust_console = Console()
    
    def require(self, name):
        with STPyV8.JSContext(Global()) as ctxt:
            name_temp = name
            if name_temp[0:2:1] == "." or name_temp[0:2:1] == "/":
                pass
            else:
                name_temp = packages[name]
            with open(name_temp, "r") as f:
                ret_val = '''
(() => {
    const module = { exports: {} };
    ((module, exports) => {
        '''+f.read()+'''
    })(module, module.exports);
    return module.exports;
})();'''
            return ctxt.eval(ret_val)

if __name__ == "__main__":
    with STPyV8.JSContext(Global()) as ctxt:
        ctxt.eval('''this.console = cust_console
        const test = require("./test.mjs");
        console.log(test.alvin("a"));
        console.log(test.name);
        ''')