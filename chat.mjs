import { OpenAI } from 'openai';
import dotenv from 'dotenv';
import readline from 'readline';

dotenv.config();

// Configuración de la API
const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY,
    organization: process.env.ORG,
});

// Función para obtener títulos de libros desde la API de la universidad
async function getBookTitles(libro) {
    const url = `https://bibliosabana.primo.exlibrisgroup.com/primaws/rest/pub/pnxs?blendFacetsSeparately=false&disableCache=false&getMore=0&inst=57US_INST&lang=es&limit=10&newspapersActive=true&newspapersSearch=false&offset=0&pcAvailability=false&q=any,contains,${libro}&qExclude=&qInclude=&rapido=false&refEntryActive=false&rtaLinks=true&scope=MyInst_and_CI&searchInFulltextUserSelection=false&skipDelivery=Y&sort=rank&tab=Everything&vid=57US_INST:US`;
    const headers = {
        "Accept": "application/json",
    };

    const response = await fetch(url, { headers });
    const parsedBody = await response.json();

    return parsedBody.docs.map(doc => doc.pnx.display.title[0]);
}

// Función para obtener información sobre un hechizo desde la API de D&D
async function getSpellInfo(spellName) {
    const url = `https://www.dnd5eapi.co/api/spells/${encodeURIComponent(spellName)}`;
    const response = await fetch(url);
    const spellData = await response.json();
    if (spellData.name === undefined) {
        console.log("No se ha encontrado el hechizo.");
        return;
    } else {
        console.log(`Claro, el hechizo "${spellData.name}" es: ${spellData.desc.join(" ")}`);
    }
}

// Función para obtener información de libros desde la API de Open Library
async function getBookInfoFromOpenLibrary(query) {
    const url = `https://openlibrary.org/search.json?q=${encodeURIComponent(query)}`;
    const response = await fetch(url);
    const data = await response.json();

    const books = data.docs.map(doc => ({
        title: doc.title,
        author_name: doc.author_name ? doc.author_name.join(', ') : 'Autor desconocido',
    }));

    return books;
}

async function getAnimeOrMangaInfo(title) {
    console.log(title);
    const url = `https://api.jikan.moe/v4/search/anime?q=${encodeURIComponent(title)}`;
    const response = await fetch(url);
    const data = await response.json();

    const animeOrManga = data.data[0];
    return {
        title: animeOrManga.title,
        tags: animeOrManga.genres.map(genre => genre.name).join(', '),
        description: animeOrManga.synopsis
    };
}

async function getBiblePassage(book, chapter, verse) {
    console.log( book, chapter, verse );
    const url = `https://api.bible/v1/bibles/06125adad2d5898a-01/verses/${book}.${chapter}.${verse}?content-type=json`;
    const headers = {
        "api-key": process.env.BIBLE_API_KEY
    };

    const response = await fetch(url, { headers });
    const data = await response.json();

    return data.data.content;
}

async function getHarryPotterInfo(type) {
    console.log(type)
    const url = `https://potterapi-fedeperin.vercel.app/en/${type}`;
    const response = await fetch(url);
    const data = await response.json();

    return data;
}




async function callChatGPTWithFunctions(userMessage) {
    let chat = await openai.chat.completions.create({
        model: "gpt-3.5-turbo",
        messages: [{
            role: "system",
            content: "Perform function request for the user",
        }, {
            role: "user",
            content: userMessage,
        }],
        functions: [{
            name: "getBookTitles",
            description: "Get book titles from the La Universidad de La Sabana University library API. Only titles and only from La Universidad de La Sabana",
            parameters: {
                type: "object",
                properties: {
                    libro: {
                        type: "string",
                        description: "The title of the book to search for, only if it's from La Universidad de La Sabana",
                    },
                },
                required: ["libro"],
                additionalProperties: false,
            }
        }, {
            name: "getSpellInfo",
            description: "Get information about a spell from the D&D API",
            parameters: {
                type: "object",
                properties: {
                    spellName: {
                        type: "string",
                        description: "The spell name must be in English, if it needs translation do it. If it consists of two or more words, remove the spaces and connect them with a hyphen ('-')",
                    },
                },
                required: ["spellName"],
                additionalProperties: false,
            }
        }, {
            name: "getBookInfoFromOpenLibrary",
            description: "Get book information (titles and authors) from Open Library API",
            parameters: {
                type: "object",
                properties: {
                    query: {
                        type: "string",
                        description: "The search query for titles or authors",
                    },
                },
                required: ["query"],
                additionalProperties: false,
            }
        }, {
            name: "getAnimeOrMangaInfo",
            description: "Get information about an anime or manga from MyAnimeList. Provides title, tags, and description.",
            parameters: {
                type: "object",
                properties: {
                    title: {
                        type: "string",
                        description: "The name of the anime or manga to search for.  If it consists of two or more words, remove the spaces and connect them with a hyphen ('-')",
                    },
                },
                required: ["title"],
                additionalProperties: false,
            }
        }, {
            name: "getBiblePassage",
            description: "Get specific passages from the Bible. Requires the book, chapter, and verse.",
            parameters: {
                type: "object",
                properties: {
                    book: {
                        type: "string",
                        description: "The book of the Bible.  If it consists of two or more words, remove the spaces and connect them with a hyphen ('-')",
                    },
                    chapter: {
                        type: "integer",
                        description: "The chapter in the book.  If it consists of two or more words, remove the spaces and connect them with a hyphen ('-')",
                    },
                    verse: {
                        type: "integer",
                        description: "The specific verse in the chapter.  If it consists of two or more words, remove the spaces and connect them with a hyphen ('-')",
                    },
                },
                required: ["book", "chapter", "verse"],
                additionalProperties: false,
            }
        }, {
            name: "getHarryPotterInfo",
            description: "Get information about Harry Potter, including books, characters, houses, and spells.",
            parameters: {
                type: "object",
                properties: {
                    type: {
                        type: "string",
                        enum: ["books", "characters", "houses", "spells"],
                        description: "The type of information to retrieve from Harry Potter: books, characters, houses, or spells.",
                    }
                },
                required: ["type"],
                additionalProperties: false,
            }
        }],
        function_call: "auto",
    });

    let wantsToUseFunction = chat.choices[0].finish_reason === "function_call";

    if (wantsToUseFunction) {
        const functionName = chat.choices[0].message.function_call.name;
        const argumentObj = JSON.parse(chat.choices[0].message.function_call.arguments);

        if (functionName === "getBookTitles") {
            let titles = await getBookTitles(argumentObj.libro);
            console.log("La universidad tiene los siguientes libros con ese título:", titles);
        } else if (functionName === "getSpellInfo") {
            await getSpellInfo(argumentObj.spellName);
        } else if (functionName === "getBookInfoFromOpenLibrary") {
            let books = await getBookInfoFromOpenLibrary(argumentObj.query);
            console.log("Encontré estos libros en Open Library:", books);
        } else if (functionName === "getAnimeOrMangaInfo") {
            let info = await getAnimeOrMangaInfo(argumentObj.title);
            console.log("Información del anime o manga:", info);
        } else if (functionName === "getBiblePassage") {
            let passage = await getBiblePassage(argumentObj.book, argumentObj.chapter, argumentObj.verse);
            console.log("Pasaje de la Biblia:", passage);
        } else if (functionName === "getHarryPotterInfo") {
            let hpInfo = await getHarryPotterInfo(argumentObj.type, argumentObj.query);
            console.log(`Información sobre ${argumentObj.type}:`, hpInfo);
        }
    } else {
        console.log("ChatGPT Response:", chat.choices[0].message.content);
    }
}


// Configuración para leer entradas desde la terminal
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

// Loop de interacción con el usuario
async function startChat() {
    console.log("ChatGPT está listo. Escribe 'exit' para salir.");

    while (true) {
        // Leer mensaje del usuario
        const userMessage = await new Promise(resolve => rl.question('> ', resolve));

        if (userMessage.toLowerCase() === 'exit') {
            console.log("Saliendo del chat...");
            rl.close();
            break;
        }

        // Llamar a la función de ChatGPT con el mensaje del usuario
        await callChatGPTWithFunctions(userMessage);
    }
}

// Iniciar el chat
startChat().catch(console.error);
