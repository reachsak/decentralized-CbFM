import React, { useState } from "react";
import axios from "axios";
import "./FileUpload.css";

import "react-awesome-button/dist/styles.css";
import {
  AwesomeButton,
  AwesomeButtonProgress,
  AwesomeButtonSocial,
} from "react-awesome-button";

// Now you can use the callPythonAPI function

const fetch = require("node-fetch");

const FileUploaddemo = ({ contract, account, provider, updateOutputText }) => {
  const [ImgHash, setImgHash] = useState(""); // State to store ImgHash

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (file) {
      try {
        const formData = new FormData();
        formData.append("file", file);

        const resFile = await axios({
          method: "post",
          url: "https://api.pinata.cloud/pinning/pinFileToIPFS",
          data: formData,
          headers: {
            pinata_api_key: `0ae4eedb33cd7e40e9c0`,
            pinata_secret_api_key: `95c11ce9c5695d0496a65ccb3aa36b9fd41e17add1f74bf600f2200cebf813f6`,
            "Content-Type": "multipart/form-data",
          },
        });

        const newImgHash = `https://gateway.pinata.cloud/ipfs/${resFile.data.IpfsHash}`;
        contract.add("0xD760A17210b61900F696ad0C21a6e11dc8884198", newImgHash);
        alert("Successfully Image Uploaded");
        console.log(newImgHash);
        setImgHash(newImgHash); // Store ImgHash in state
        setFileName("No image selected");
        setFile(null);
      } catch (e) {
        alert("Unable to upload image to Pinata");
      }
    }
  };

  const retrieveFile = (e) => {
    const data = e.target.files[0];
    const reader = new window.FileReader();
    reader.readAsArrayBuffer(data);
    reader.onloadend = () => {
      setFile(e.target.files[0]);
    };
    setFileName(e.target.files[0].name);
  };

  const [file, setFile] = useState(null);
  const [fileName, setFileName] = useState("None");

  return (
    <div className="top">
      <div>
        <h2>Upload image</h2>
      </div>
      <form className="form" onSubmit={handleSubmit}>
        <AwesomeButton
          type="twitter"
          onPress={() => document.getElementById("file-upload").click()}
          // Add class for styling
        >
          Choose Image
        </AwesomeButton>

        <input
          disabled={!account}
          type="file"
          id="file-upload"
          name="data"
          onChange={retrieveFile}
        />
        <div>
          <span className="textArea" style={{ color: "black" }}>
            Image: {fileName}{" "}
          </span>
        </div>

        <div>
          <AwesomeButton type="primary" disabled={!file}>
            Upload File
          </AwesomeButton>
        </div>
      </form>
      <div>
        <div>
          {file && (
            <img
              src={URL.createObjectURL(file)}
              alt="Preview"
              style={{ maxWidth: "100%", height: "auto" }}
            />
          )}
        </div>
      </div>
    </div>
  );
};

export default FileUploaddemo;
