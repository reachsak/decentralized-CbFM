(function () {
  "use strict";

  var sdk = require("microsoft-cognitiveservices-speech-sdk");
  var readline = require("readline");
  var Speaker = require("speaker");

  // This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
  const speechConfig = sdk.SpeechConfig.fromSubscription(
    "5630d19384fc422f88c86b91e2354aee",
    "eastus"
  );

  // The language of the voice that speaks.
  speechConfig.speechSynthesisVoiceName = "en-US-AvaMultilingualNeural";

  // Create the speech synthesizer.
  var synthesizer = new sdk.SpeechSynthesizer(speechConfig);

  var rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  var tts =
    "Angkor Wat is a Hindu-Buddhist temple complex in Cambodia. Located on a site measuring 162.6 hectares within the ancient Khmer capital city of Angkor, it is considered as the largest religious structure in the world by Guinness World Records.";

  synthesizer.speakTextAsync(
    tts,
    function (result) {
      if (result.reason === sdk.ResultReason.SynthesizingAudioCompleted) {
        console.log("Speech synthesis completed.");
        playSpeech(Buffer.from(result.audioData)); // Convert ArrayBuffer to Buffer
      } else {
        console.error(
          "Speech synthesis canceled, " +
            result.errorDetails +
            "\nDid you set the speech resource key and region values?"
        );
      }
      synthesizer.close();
    },
    function (err) {
      console.trace("err - " + err);
      synthesizer.close();
    }
  );

  // Function to play the synthesized speech directly
  function playSpeech(audioData) {
    var speaker = new Speaker({
      channels: 1,
      bitDepth: 16,
      sampleRate: 16000,
    });
    speaker.end(audioData);
  }
})();
