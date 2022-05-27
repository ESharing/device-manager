export function getUrlKey(name,url){
    return decodeURIComponent(
        (new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(url) || ["",""])[1].replace(/\+/g, '%20')) || null
}

export function isValidIPv4(ip)
{
var reg = /^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/
return reg.test(ip);
}
 export function isValidPort(port) 
 {
    if ( Number.isNaN(port) )
        return false
    var portNum = parseInt(port,10)
    if (portNum>65535 || portNum < 1) 
        return false
    
    return true    
 }