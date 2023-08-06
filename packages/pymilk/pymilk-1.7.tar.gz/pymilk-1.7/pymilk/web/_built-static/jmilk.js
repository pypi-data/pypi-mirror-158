
class jmilk {

    static timestamp = () => Date.parse(new Date()) / 1000
    static timestampMilli = () => Date.parse(new Date())

    static ID = elementId => document.getElementById(elementId)

    static sleep = (second) => {
        let last = jmilk.timestampMilli() + second * 1000
        while (jmilk.timestampMilli() < last) {}
    }

    static asleep = (second) => new Promise((resolve) => {setTimeout(resolve, second * 1000)})
    
    static inKeys = (obj, iterator) => {
        for (let i in iterator) {
            if (i === obj) { return true }
        }
        return false
    }

    static inValues = (obj, iterator) => {
        for (let i in iterator) {
            if (iterator[i] === obj) { return true }
        }
        return false
    }

    static getMD5 = string => CryptoJS.MD5(string).toString()
    
    static bodyAddToken = (body, token) => {
        let sbodyJson = JSON.stringify({
            body: body,
            reqBatch: Math.random().toString() + Math.random().toString(),
            timestamp: jmilk.timestamp()
        })
        return JSON.stringify({
            sbodyJson: sbodyJson,
            hash: jmilk.getMD5(sbodyJson + token)
        })  // return gbodyJson
    }

    static post = (url, body = null) => {
        var req = new XMLHttpRequest()
        req.open("POST", url, false)
        req.send(body)
        return req.responseText
    }
    static postJson = (url, body = null) => JSON.parse(jmilk.post(url, JSON.stringify(body)))
    
    static get = (url) => {
        var req = new XMLHttpRequest()
        req.open("GET", url, false)
        req.send()
        return req.responseText
    }
    static getJson = (url) => JSON.parse(jmilk.get(url))
    
    static numberStrRange = (start, end) => {
        var dic = {}
        var i = start - 1
        while (true) {
            i = i + 1
            if (i <= end) {dic[i] = 0}
            else {return dic}
        }
    }
}