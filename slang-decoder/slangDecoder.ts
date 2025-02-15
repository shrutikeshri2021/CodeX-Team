/*import axios from 'axios';

class SlangDecoder {
    private apiKey: string;
    private baseURL: string;

    constructor(apiKey: string) {
        this.apiKey = apiKey;
        this.baseURL = 'https://api.urbandictionary.com/v0/define?term=';
    }

    public async decode(slang: string): Promise<string> {
        try {
            const response = await axios.get(`${this.baseURL}${encodeURIComponent(slang)}`, {
                headers: {
                    'Authorization': `Bearer ${this.apiKey}`
                }
            });

            if(response.data.list && response.data.list.length > 0) {
                return response.data.list[0].definition;
            } else {
                return `No definition found for ${slang}`;
            }
        } catch (error: any) { 
            console.error(`Error decoding slang: ${error}`);
            return `Error decoding slang: ${error.message}`;
        }
    }
}

// Usage example:
const apiKey = 'YOUR_GOOGLE_GEMINI_API_KEY';
const decoder = new SlangDecoder(apiKey);

decoder.decode('rizzzz').then((definition) => {
    console.log(`🔥 Slang Word: 'rizzzz'\n💬 Definition: ${definition}`);
}).catch((error) => {
    console.error(error);
});*/

