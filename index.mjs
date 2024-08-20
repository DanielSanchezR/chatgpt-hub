import { OpenAI } from 'openai';

// Configuración de la API
const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY,
    organization: process.env.ORG,
});

// Función para obtener títulos de libros desde la API de la biblioteca
async function getBookTitles(libro) {
    const url = `https://bibliosabana.primo.exlibrisgroup.com/primaws/rest/pub/pnxs?blendFacetsSeparately=false&disableCache=false&getMore=0&inst=57US_INST&lang=es&limit=10&newspapersActive=true&newspapersSearch=false&offset=0&pcAvailability=false&q=any,contains,${libro}&qExclude=&qInclude=&rapido=false&refEntryActive=false&rtaLinks=true&scope=MyInst_and_CI&searchInFulltextUserSelection=false&skipDelivery=Y&sort=rank&tab=Everything&vid=57US_INST:US`;
    const headers = {
        "Accept": "application/json",
    };

    const response = await fetch(url, { headers });
    const parsedBody = await response.json();

    return parsedBody.docs.map(doc => doc.pnx.display.title[0]);
}

// Función para llamar a ChatGPT con funciones
async function callChatGPTWithFunctions(libro) {
    let chat = await openai.chat.completions.create({
        model: "gpt-3.5-turbo",
        messages: [{
            role: "system",
            content: "Perform function request for the user",
        }, {
            role: "user",
            content: `Hello, I am a user, I would like to search for a book titled '${libro}' and get the titles from the library API.`,
        }],
        functions: [{
            name: "getBookTitles",
            description: "Get book titles from the library API",
            parameters: {
                type: "object",
                properties: {
                    libro: {
                        type: "string",
                        description: "The title of the book to search for",
                    },
                },
                required: ["libro"],
                additionalProperties: false,
            }
        }],
        function_call: "auto",
    });

    let wantsToUseFunction = chat.choices[0].finish_reason === "function_call";

    if (wantsToUseFunction) {
        if (chat.choices[0].message.function_call.name === "getBookTitles") {
            let argumentObj = JSON.parse(chat.choices[0].message.function_call.arguments);
            let titles = await getBookTitles(argumentObj.libro);
            console.log("Book Titles:", titles);
        }
    }
}

// Llamada a la función con el título del libro "Cien años de soledad"
callChatGPTWithFunctions("Cien años de soledad").catch(console.error);
