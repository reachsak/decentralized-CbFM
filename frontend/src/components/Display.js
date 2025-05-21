import { useState } from "react";
import axios from "axios";
import "./Display.css";
import "react-awesome-button/dist/styles.css";
import Box from "@mui/material/Box";
import {
  AwesomeButton,
  AwesomeButtonProgress,
  AwesomeButtonSocial,
} from "react-awesome-button";
const Display = ({ contract, account, propDesc }) => {
  const proposalDescription = propDesc || "Default Description";
  const [ImgHash, setImgHash] = useState(""); // State to store ImgHash

  const [data, setData] = useState("");

  const getdata = async (address) => {
    let dataArray;
    try {
      if (address) {
        dataArray = await contract.display(address);
        console.log(dataArray);
      } else {
        dataArray = await contract.display(account);
        console.log(dataArray);
        console.log(proposalDescription);
      }
    } catch (e) {
      alert("You don't have access");
    }

    const isEmpty = Object.keys(dataArray).length === 0;

    if (!isEmpty) {
      const str = dataArray.toString();
      const str_array = str.split(",");
      const lastImage = str_array[str_array.length - 1];
      const lastImageElement = (
        <a href={lastImage} target="_blank">
          <img src={lastImage} alt="new" className="image-list" />
        </a>
      );
      setData([lastImageElement]);
      setImgHash(lastImage);
    } else {
      alert("No image to display");
    }
  };

  return (
    <>
      <div className="description-box">
        <Box
          boxShadow={3}
          bgcolor="background.paper"
          p={2}
          className="retro-box" // Add a class for retro style
          maxWidth="fit-content" // Set maximum width to fit the content
          margin="auto" // Center the box horizontally
          display="flex"
          flexDirection="column"
          alignItems="center" // Center the content vertically
        >
          <p>{proposalDescription}</p>
        </Box>
      </div>
      <div className="image-list">{data}</div>

      <AwesomeButton type="facebook" onPress={() => getdata()}>
        Get latest submission
      </AwesomeButton>
    </>
  );
};

export default Display;
