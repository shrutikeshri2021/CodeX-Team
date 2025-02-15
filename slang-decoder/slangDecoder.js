"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const axios_1 = __importDefault(require("axios"));
class SlangDecoder {
    constructor(apiKey) {
        this.apiKey = apiKey;
        this.baseURL = 'https://api.urbandictionary.com/v0/define?term=';
    }
    decode(slang) {
        return __awaiter(this, void 0, void 0, function* () {
            try {
                const response = yield axios_1.default.get(`${this.baseURL}${encodeURIComponent(slang)}`, {
                    headers: {
                        'Authorization': `Bearer ${this.apiKey}`
                    }
                });
                if (response.data.list && response.data.list.length > 0) {
                    return response.data.list[0].definition;
                }
                else {
                    return `No definition found for ${slang}`;
                }
            }
            catch (error) {
                console.error(`Error decoding slang: ${error}`);
                return `Error decoding slang: ${error.message}`;
            }
        });
    }
}
// Usage example:
const apiKey = 'YOUR_GOOGLE_GEMINI_API_KEY';
const decoder = new SlangDecoder(apiKey);
decoder.decode('vibe').then((definition) => {
    console.log(`🔥 Slang Word: 'vibe'\n💬 Definition: ${definition}`);
}).catch((error) => {
    console.error(error);
});
