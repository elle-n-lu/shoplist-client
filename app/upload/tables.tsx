"use client";
import axios, { AxiosError } from "axios";
import { useRouter, useSearchParams } from "next/navigation";
import React, { useCallback, useState } from "react";
import { ToastContainer, toast } from "react-toastify";
import { plans } from "../plans/page";

export interface tablesProps {
  id: number;
  budget: number;
  file_name: string;
  date: string;
  addMessage: (mes:string)=>void
  plans: plans
}
const Tables: React.FC<tablesProps> = ({
  id,
  budget,
  file_name,
  date,
  addMessage,
  plans
}) => {
  
  const [message, setMessage]= useState('')
  const changeMessage=(mes:string)=>{
    setMessage(mes)
    addMessage(mes)
  }
  const token =
    typeof window !== "undefined" && (localStorage.getItem("access") as string);
  const deleteOp = async (id: number) => {
    await axios
      .delete("http://127.0.0.1:5000/files/delete/" + id, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) =>{changeMessage('added'); window.location.reload()})
      .catch((error) => {console.log(error.response.data.detail);changeMessage(error.response.data.detail)});
  };
  const router = useRouter();
  const searchParams:any = useSearchParams()!
  const createQueryString = useCallback(
    ( name:string, value: string) => {
      const params = new URLSearchParams(searchParams)
      params.set(name, value)
      return params.toString()
    },
    [searchParams]
  )
 
  return (
    <>
      <tr
        className="bg-white border-b dark:text-white dark:bg-gray-600 "
        key={id}
      >
        <th
          scope="row"
          className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white"
        >
          {budget}
        </th>
        <td className="px-6 py-4">{file_name}</td>
        <td className="px-6 py-4"><button className="hover:text-blue-500 hover:underline" onClick={()=>{
          
          router.push('/plans'+ '?' + createQueryString("plans", JSON.stringify(plans)))
        }}>results</button></td>

        <td className="px-6 py-4">{date}</td>
        <td>
          <button
          className="hover:text-red-500"
            onClick={() => {
              deleteOp(id);
            }}
          >
            delete
          </button>
        </td>
      </tr>
    </>
  );
};
export default Tables;
