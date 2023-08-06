"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
var __values = (this && this.__values) || function(o) {
    var s = typeof Symbol === "function" && Symbol.iterator, m = s && o[s], i = 0;
    if (m) return m.call(o);
    if (o && typeof o.length === "number") return {
        next: function () {
            if (o && i >= o.length) o = void 0;
            return { value: o && o[i++], done: !o };
        }
    };
    throw new TypeError(s ? "Object is not iterable." : "Symbol.iterator is not defined.");
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
exports.__esModule = true;
/* -*- javascript -*- */
var soundswallower_js_1 = __importDefault(require("./soundswallower.js"));
var fs_1 = require("fs");
var assert = __importStar(require("assert"));
(function () { return __awaiter(void 0, void 0, void 0, function () {
    var soundswallower, config, nkeys, config_1, config_1_1, key, decoder, pcm, hyp, hypseg, hypseg_words, hypseg_1, hypseg_1_1, seg, fsg;
    var e_1, _a, e_2, _b;
    return __generator(this, function (_c) {
        switch (_c.label) {
            case 0: return [4 /*yield*/, (0, soundswallower_js_1["default"])()];
            case 1:
                soundswallower = _c.sent();
                config = new soundswallower.Config();
                console.log(config.get("samprate"));
                nkeys = 0;
                try {
                    for (config_1 = __values(config), config_1_1 = config_1.next(); !config_1_1.done; config_1_1 = config_1.next()) {
                        key = config_1_1.value;
                        ++nkeys;
                    }
                }
                catch (e_1_1) { e_1 = { error: e_1_1 }; }
                finally {
                    try {
                        if (config_1_1 && !config_1_1.done && (_a = config_1["return"])) _a.call(config_1);
                    }
                    finally { if (e_1) throw e_1.error; }
                }
                console.log("Found ".concat(nkeys, " keys in config"));
                decoder = new soundswallower.Decoder({
                    fsg: "testdata/goforward.fsg",
                    samprate: 16000
                });
                return [4 /*yield*/, decoder.initialize()];
            case 2:
                _c.sent();
                return [4 /*yield*/, fs_1.promises.readFile("testdata/goforward-float32.raw")];
            case 3:
                pcm = _c.sent();
                return [4 /*yield*/, decoder.start()];
            case 4:
                _c.sent();
                return [4 /*yield*/, decoder.process(pcm, false, true)];
            case 5:
                _c.sent();
                return [4 /*yield*/, decoder.stop()];
            case 6:
                _c.sent();
                hyp = decoder.get_hyp();
                console.log("recognized: ".concat(hyp));
                assert.equal("go forward ten meters", hyp);
                hypseg = decoder.get_hypseg();
                hypseg_words = [];
                try {
                    for (hypseg_1 = __values(hypseg), hypseg_1_1 = hypseg_1.next(); !hypseg_1_1.done; hypseg_1_1 = hypseg_1.next()) {
                        seg = hypseg_1_1.value;
                        assert.ok(seg.end >= seg.start);
                        if (seg.word != "<sil>" && seg.word != "(NULL)")
                            hypseg_words.push(seg.word);
                    }
                }
                catch (e_2_1) { e_2 = { error: e_2_1 }; }
                finally {
                    try {
                        if (hypseg_1_1 && !hypseg_1_1.done && (_b = hypseg_1["return"])) _b.call(hypseg_1);
                    }
                    finally { if (e_2) throw e_2.error; }
                }
                assert.deepStrictEqual(hypseg_words, ["go", "forward", "ten", "meters"]);
                /* Test create_fsg */
                return [4 /*yield*/, decoder.add_word("_go", "G OW", false)];
            case 7:
                /* Test create_fsg */
                _c.sent();
                return [4 /*yield*/, decoder.add_word("_forward", "F AO R W ER D", false)];
            case 8:
                _c.sent();
                return [4 /*yield*/, decoder.add_word("_ten", "T EH N", false)];
            case 9:
                _c.sent();
                return [4 /*yield*/, decoder.add_word("_meters", "M IY T ER Z", true)];
            case 10:
                _c.sent();
                fsg = decoder.create_fsg("goforward", 0, 4, [
                    { from: 0, to: 1, prob: 1.0, word: "_go" },
                    { from: 1, to: 2, prob: 1.0, word: "_forward" },
                    { from: 2, to: 3, prob: 1.0, word: "_ten" },
                    { from: 3, to: 4, prob: 1.0, word: "_meters" }
                ]);
                return [4 /*yield*/, decoder.set_fsg(fsg)];
            case 11:
                _c.sent();
                fsg["delete"](); // has been retained by decoder
                return [4 /*yield*/, fs_1.promises.readFile("testdata/goforward-float32.raw")];
            case 12:
                pcm = _c.sent();
                return [4 /*yield*/, decoder.start()];
            case 13:
                _c.sent();
                return [4 /*yield*/, decoder.process(pcm, false, true)];
            case 14:
                _c.sent();
                return [4 /*yield*/, decoder.stop()];
            case 15:
                _c.sent();
                hyp = decoder.get_hyp();
                console.log("recognized: ".concat(hyp));
                assert.equal("_go _forward _ten _meters", hyp);
                /* Test JSGF */
                fsg = decoder.parse_jsgf("#JSGF V1.0;\ngrammar pizza;\npublic <order> = [<greeting>] [<want>] [<quantity>] [<size>] [<style>]\n       [(pizza | pizzas)] [<toppings>];\n<greeting> = hi | hello | yo | howdy;\n<want> = i want | gimme | give me | i'd like to order | order | i wanna;\n<quantity> = a | one | two | three | four | five;\n<size> = small | medium | large | extra large | x large | x l;\n<style> = hawaiian | veggie | vegetarian | margarita | meat lover's | all dressed;\n<toppings> = [with] <topping> ([and] <topping>)*;\n<topping> = pepperoni | ham | olives | mushrooms | tomatoes | (green | hot) peppers | pineapple;\n");
                return [4 /*yield*/, decoder.set_fsg(fsg)];
            case 16:
                _c.sent();
                fsg["delete"]();
                return [4 /*yield*/, fs_1.promises.readFile("testdata/pizza-float32.raw")];
            case 17:
                pcm = _c.sent();
                return [4 /*yield*/, decoder.start()];
            case 18:
                _c.sent();
                return [4 /*yield*/, decoder.process(pcm, false, true)];
            case 19:
                _c.sent();
                return [4 /*yield*/, decoder.stop()];
            case 20:
                _c.sent();
                hyp = decoder.get_hyp();
                console.log("recognized: ".concat(hyp));
                assert.equal("yo gimme four large all dressed pizzas", hyp);
                decoder["delete"]();
                return [2 /*return*/];
        }
    });
}); })();
