


function i() {
    var t = Math.floor((new Date).getTime() / 1e3)
      , e = t.toString(16).toUpperCase()
      , n = (0, s.default)(t).toString().toUpperCase();
    if (8 != e.length)
        return {
            as: "479BB4B7254C150",
            cp: "7E0AC8874BB0985"
        };
    for (var r = n.slice(0, 5), i = n.slice(-5), o = "", a = 0; a < 5; a++)
        o += r[a] + e[a];
    for (var u = "", l = 0; l < 5; l++)
        u += e[l + 3] + i[l];
    return {
        as: "A1" + o + e.slice(-3),
        cp: e.slice(0, 3) + u + "E1"
    }
}

