"use client";
import axios from "axios";
import Link from "next/link";
import { useRouter } from "next/navigation";
import React, { useState } from "react";
import { base_api } from "../base_api/base_api";
interface pageProps {}
const Page: React.FC<pageProps> = () => {
  const router = useRouter();
  let token: string;
  if (typeof window !== "undefined") {
    token = localStorage.getItem("access") as string;
  }
  // input budget and upload file
  const [budget, setBudget] = useState("");
  const [file, setFile] = useState("");
  const [fileErrors, setFileErrors] = useState<string>("");
  // input data and file upload to server
  const dataUpload = async (e: any) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("budget", budget);
    formData.append("uploadfile", file);
    await axios
      .post(base_api+"files/upload", formData, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => router.push('/'))
      .catch(async (error) => {
        console.log(error.response.data[0]);
      })
  };

  // change file and validate file format
  const fileChange = (e: any) => {
    const file = e.target.files[0];
    const lens = file.name.split(".").length;
    const format = file.name.split(".")[lens - 1].toLowerCase();
    if (file != "" && !["txt"].includes(format)) {
      setFileErrors("Only txt files are allowed");
    } else {
      setFile(e.target.files[0]);
      setFileErrors("");
    }
  };

  return (
    <div
      className="bg-blue-200 flex mx-auto justify-center pt-10 "
      style={{ height: "100vh" }}
    >
      <Link href="/">
        <button className="bg-blue-500 p-2 rounded-md mr-2">Back</button>
      </Link>
      <form
        className="flex flex-col bg-white p-10 rounded-lg max-h-96"
        onSubmit={dataUpload}
      >
        <div>
          <p>Budget</p>
          <input
            type="number"
            className="border-purple-500 border-2 mt-2 py-1 rounded-md"
            // value={budget}
            onChange={(e) => setBudget(e.target.value)}
            required
          />
        </div>
        <div className=" mt-2 py-2 ">
          <label>Shoplist file selection:</label>
          <label className="block mt-2 h-10">
            <span className="sr-only">Choose choose shoplist txt file</span>
            <input
              required
              type="file"
              onChange={fileChange}
              className="block w-full text-sm text-slate-500
      file:mr-4 file:py-2 file:px-4
      file:rounded-full file:border-0
      file:text-sm file:font-semibold
      file:bg-violet-50 file:text-violet-700
      hover:file:bg-violet-100
    "
            />
          </label>
          <p className="text-red-500">{fileErrors}</p>
        </div>
        <button
          type="submit"
          value="submit"
          className="bg-purple-500 w-1/2 rounded-md p-2 text-white hover:bg-purple-600 hover:shadow-lg hover:shadow-purple-900"
        >
          Submit
        </button>
      </form>
    </div>
  );
};
export default Page
