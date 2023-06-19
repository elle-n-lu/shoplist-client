"use client";
import Link from "next/link";
import axios from "axios";
import Tables from "./upload/tables";
import { tablesProps } from "./upload/tables";
import { useEffect, useState } from "react";
import { ToastContainer, toast } from "react-toastify";
import { useRouter } from "next/navigation";
import "react-toastify/dist/ReactToastify.css";
const Home = () => {
  const router = useRouter();
  const notify = (message: string) => toast(message);
  const [username, setUsername] = useState<string | undefined>();
  const token =
    typeof window !== "undefined" && (localStorage.getItem("access") as string);
  const [message, setMessage] = useState("");
  const [file, setFile] = useState<tablesProps[] | null>(null);
  const addChildMessage = (val: string) => {
    setMessage(val);
  };
  const clickget = async () => {
    await axios
      .get("http://127.0.0.1:5000/files/", {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
        setFile(res.data);
      })
      .catch(async (error) => {
        // console.log(error.response.data.code);
        notify(error.response.data.code);
      });
  };

  const logout=(e:any)=>{
    e.preventdefault;
    localStorage.removeItem("access");
    localStorage.removeItem("user");
    router.refresh()
  }

  useEffect(() => {
    if (typeof window !== "undefined") {
      if (!localStorage.getItem("access")) {
        router.push("/signin");
      } else {
        setUsername(localStorage.getItem("user") as string);
      }
    }

    clickget();
  }, []);

  useEffect(() => {
    if (message !== "") {
      notify(message);
    }
  });

  return (
    <div className="container mx-auto text-center pt-10">
      <ToastContainer />
      <div className="grid grid-cols-4 ">
        <div className="col-span-1 justify-items-center justify-self-center">
          {username ? (
            <>
            <button className="rounded-full border-blue-500 border hover:shadow-md w-12 h-12">
              {username}
            </button>
            <button onClick={logout} className="text-gray-400 hover:text-gray-500 hover:underline ml-4">Exit</button>
            </>
          ) : (
            <>
              {" "}
              <Link href="/signin">
                {" "}
                <button className="p-2 bg-blue-300 rounded-l-lg mr-2 hover:text-white hover:bg-blue-500 hover:shadow-blue-500 hover:shadow-lg">
                  Sign In
                </button>
              </Link>
              <Link href="/register">
                <button className="p-2 bg-blue-300 rounded-r-lg hover:text-white hover:bg-blue-500 hover:shadow-blue-500  hover:shadow-lg">
                  Sign Up
                </button>
              </Link>
            </>
          )}
        </div>
        <div className="col-span-"></div>
        <h1 className="col-span-2 text-3xl">
          New Budget shop plan
          <Link href="/upload">
            <button className="bg-blue-500 w-8 rounded-r-lg ml-2">+</button>
          </Link>
        </h1>
      </div>
      {/* <button onClick={clickget}>clickget</button> */}

      {/* map retrive budget and shop txtfile info here */}
      {file && (
        <div className="relative overflow-x-auto pt-10">
          <table className="w-full text-sm text-left text-gray-500">
            <thead className="text-xs text-gray-700 uppercase bg-gray-50 ">
              <tr>
                <th scope="col" className="px-6 py-3">
                  budget
                </th>
                <th scope="col" className="px-6 py-3">
                  txt file
                </th>
                <th scope="col" className="px-6 py-3">
                  plan_results
                </th>
                <th scope="col" className="px-6 py-3">
                  date
                </th>
                <th scope="col" className=" py-3">
                  operation
                </th>
              </tr>
            </thead>
            <tbody>
              {file.map((item: tablesProps, index: number) => (
                <Tables
                  id={item.id}
                  budget={item.budget}
                  date={item.date}
                  file_name={item.file_name}
                  key={index}
                  addMessage={addChildMessage}
                  plans={item.plans}
                />
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};
export default Home;
