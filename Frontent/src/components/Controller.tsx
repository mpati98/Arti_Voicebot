import { useState } from "react";
import Title from "./Title";
import RecordMessage from "./RecordMessage";
import axios from "axios";

function Controller() {
    const [isLoading, setIsLoading] = useState(false);
    const [messages, setMessages] = useState<any[]>([]);

    const createBlobUrl = (data: any) => {
        const blob = new Blob([data], { type: "audio/mpeg" });
        const url = window.URL.createObjectURL(blob);
        return url;
    }

    const handleStop = async (blobUrl: string) => {
        setIsLoading(true)

        // Append recorded message to messages
        const myMessage = { sender: "me", blobUrl };
        const messagesArr = [...messages, myMessage];

        // Convert blob url to blob object
        fetch(blobUrl)
            .then((res) => res.blob())
            .then(async (blob) => {
                // Construct audio to send file
                const formData = new FormData();
                formData.append("file", blob, 'myAudioFile.wav');

                // Send form data to API endpoint
                await axios.post("http://localhost:8000/post-audio", formData, {
                    headers: {
                        "Content-Type": "audio/mpeg"
                    },
                    responseType: "arraybuffer"
                })
                    .then((res: any) => {
                        const blob = res.data;
                        const audio = new Audio();
                        audio.src = createBlobUrl(blob);

                        // Append to audio
                        const ArtiMessage = { sender: "arti", blobUrl: audio.src };
                        messagesArr.push(ArtiMessage);
                        setMessages(messagesArr);

                        // Play Audio
                        setIsLoading(false);
                        audio.play();
                    }).catch(err => console.log(err));
            })

        setIsLoading(false)
    }

    return (
        <div className="h-screen overflow-y-hidden">
            <Title setMessages={setMessages} />
            <div className="flex flex-col justify-between h-full overflow-y-scroll pb-96">
                {/* Conversation */}
                <div className="mt-5 px-5">
                    {
                        messages.map((audio, index) => {
                            console.log(audio.sender);
                            return(
                                <div key={index + audio.sender}
                                className={
                                    "flex flex-col" + 
                                    (audio.sender == "me" && "flex flex-col items-end")
                                }
                                >
                                    {/* Sender */}
                                    <div className="mt-4">
                                        <p
                                            className={
                                                audio.sender === 'me' ? 
                                                "text-right mr-2 italic text-green-500" : "ml-2 italic text-blue-500"
                                            }
                                        >{audio.sender}
                                        </p>

                                        {/* Audio Message */}
                                            <audio src={audio.blobUrl}
                                            className="appearance-none" controls></audio>

                                    </div>

                                </div>
                            )
                        
                    })}

                    {/* loading response */}
                    {
                        messages.length == 0 && !isLoading && (
                            <div className="text-center font-light italic mt-10">
                                Send Arti a message ...
                            </div>
                        )
                    }

                    {
                        isLoading && (
                            <div className="text-center font-light italic mt-10 animate-pluse">
                                Give me a few seconds ...
                            </div>
                        )
                    }

                </div>

                {/* Recorder */}
                <div className="fixed bottom-0 w-full py-6 border-t text-center bg-gradient-to-r from-sky-500 to-green-500">
                    <div className="flex justify-center items-center w-full">
                        <RecordMessage handleStop={handleStop} />
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Controller