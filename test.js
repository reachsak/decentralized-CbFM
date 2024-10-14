import React, { useEffect, useState, useRef } from "react";
import "./Display.css";
import Box from "@mui/material/Box";
const Groq = require("groq-sdk");
const groq = new Groq({
  dangerouslyAllowBrowser: true,
  apiKey: "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",
});
export const Chatvoiceollamagroq = () => {
  const [history, setHistory] = useState([]);
  const [prompt, setPrompt] = useState("");
  const [context, setContext] = useState([]);
  const [loading, setLoading] = useState(false);
  const [transcribedText, setTranscribedText] = useState("");
  const [isRecording, setIsRecording] = useState(false);

  const recognition = useRef(null);
  const chatBoxRef = useRef(null);
  const [socket, setSocket] = useState(null);
  const [audio, setAudio] = useState(null);
  const getGroqChatCompletion = async (prompt) => {
    return groq.chat.completions.create({
      messages: [
        {
          role: "system",
          content: "you are a helpful assistant.",
        },
        {
          role: "user",
          content: prompt,
        },
      ],
      model: "mixtral-8x7b-32768",
      temperature: 0.5,
      max_tokens: 2048,
      top_p: 1,
      stop: null,
      stream: false,
    });
  };

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8795");
    setSocket(ws);

    return () => {
      ws.close();
    };
  }, []);
  useEffect(() => {
    if (socket) {
      socket.addEventListener("message", function (event) {
        console.log("Received audio from server");
        setAudio(URL.createObjectURL(event.data));
      });
    }
  }, [socket]);
  const convertTextToSpeech = async (text) => {
    // Send text to the server for text-to-speech conversion
    if (socket && socket.readyState === WebSocket.OPEN) {
      // Replace full stops with a unique delimiter
      const text1 = text.replace(/\n+/g, ".");
      const formattedText = text1.replace(/\./g, ",");
      const formattedText2 = formattedText.replace(/n't/g, "not");
      const formattedText3 = formattedText2.replace(/\'/g, ",");
      const formattedText4 = formattedText3.replace(/\!/g, ",");
      const formattedText5 = formattedText4.replace(/\:/g, ",");

      console.log(formattedText5);

      socket.send(formattedText5);
    } else {
      console.error("WebSocket connection not established");
    }
  };

  const handleStartRecording = () => {
    setIsRecording(true);
    recognition.current.start();
  };

  const handleStopRecording = () => {
    setIsRecording(false);
    recognition.current.stop();
  };

  useEffect(() => {
    recognition.current = new window.webkitSpeechRecognition();
    recognition.current.continuous = false;
    recognition.current.interimResults = false;
    recognition.current.lang = "en-US";

    recognition.current.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setTranscribedText(transcript);
    };

    recognition.current.onerror = (event) => {
      console.error("Speech recognition error:", event.error);
      setIsRecording(false);
    };
  }, []);
  useEffect(() => {
    if (transcribedText) {
      setPrompt(transcribedText);
    }
  }, [transcribedText]);

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      document.getElementById("sendButton").click();
    }
  };

  useEffect(() => {
    chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
  }, [history]);

  const sendPrompt = async () => {
    setLoading(true);
    const tempHistory = [
      ...history,
      { prompt, type: "user", timestamp: Date.now() },
    ];
    setHistory(tempHistory);

    try {
      const chatCompletion = await getGroqChatCompletion(prompt);
      const content = chatCompletion.choices[0]?.message?.content || "";
      console.log(content);

      const reader = content?.getReader();
      if (reader) {
        let serverResponse = "";

        while (true) {
          const { value, done } = await reader.read();
          if (done) {
            setLoading(false);
            break;
          }

          const decodedValue = new TextDecoder("utf-8").decode(value);

          try {
            const { response, done, context } = JSON.parse(decodedValue);

            if (response) {
              serverResponse += response;
              tempHistory[tempHistory.length - 1].prompt = serverResponse;
              setHistory([...tempHistory]);
            }

            if (done) {
              setPrompt(""); // Clear prompt after receiving server response
              setContext(content);
            }
          } catch (e) {
            console.error(e);
          }
        }
        convertTextToSpeech(serverResponse);
      }
    } catch (error) {
      console.error("Error sending prompt:", error);
      setLoading(false);
    }
  };

  return (
    <div>
      <Box
        boxShadow={3}
        bgcolor="background.paper"
        p={2}
        className="retro-box"
        maxWidth="fit-content"
        margin="auto"
        display="flex"
        flexDirection="column"
        alignItems="center"
      >
        <div className="App">
          <Box
            boxShadow={3}
            bgcolor="background.paper"
            p={2}
            className="retro-box"
            maxWidth="1000px"
            margin="auto"
            display="flex"
            flexDirection="column"
            alignItems="center"
          >
            <p1>ChatBot with Groq</p1>
            <div ref={chatBoxRef} className="chat-box">
              <div className="history">
                {history.map((item, index) => (
                  <div key={index} className={`message ${item.type}`}>
                    {item.type === "user" ? "🧑🏻‍💻Sak:" : "🤖AI:"} {item.prompt}
                  </div>
                ))}
              </div>
            </div>
          </Box>
          <div>
            <textarea
              className="textarea"
              placeholder="Let's chat"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              onKeyPress={handleKeyPress}
            ></textarea>
          </div>
          <div className="send-button-container">
            <button
              id="sendButton"
              className={`send-button ${loading ? "disabled" : ""}`}
              disabled={loading}
              onClick={sendPrompt}
            >
              Send
            </button>
            {isRecording ? (
              <button onClick={handleStopRecording}>Stop Recording</button>
            ) : (
              <button onClick={handleStartRecording}>Start Recording</button>
            )}
          </div>
        </div>
      </Box>
      {audio && <audio src={audio} controls />}
      {audio && <audio src={audio} autoPlay />}
    </div>
  );
};
