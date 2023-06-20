"use client";
import React, { useEffect, useState } from "react";
import Card from "./card";
import { useRouter, useSearchParams } from "next/navigation";
type list_of_items = {
  price: string;
  title: string;
};
type cost={
  total_cost:string
}
export type plans = {
  list_of_items: list_of_items[];
  cost: cost
};
// type planProps = {
//   plans: plans[];
// };
const Page: React.FC = () => {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [plans, setPlans] = useState<plans[]>([]);

  useEffect(() => {
    if (searchParams) {
      setPlans(JSON.parse(searchParams.get("plans") as string) as plans[]);
    }
  }, [searchParams]);
  return (
    <div className="flex flex-col mt-12 mx-auto w-3/4">
      <div className="flex items-center justify-evenly">
        <button
          className="bg-blue-400 text-white p-2 rounded-md"
          onClick={() => router.push("/")}
        >
          Home
        </button>
        <h5 className="text-2xl font-bold text-gray-900 ">
          {" "}
          Shopping Plans for your list
        </h5>
        <a
          href="#"
          className="text-lg font-medium text-blue-600 hover:underline "
        >
          View all
        </a>
        <div className="flex items-center">
          <input
            type="text"
            className="bg-gray-50 p-2 border border-gray-300 text-gray-900 text-sm rounded-sm focus:ring-blue-500 focus:border-blue-500"
            placeholder="write your comment"
          />
          <button className="ml-2 p-2 rounded-md bg-green-600 text-white">Comment</button>
        </div>
      </div>
      <div className="grid grid-cols-4 gap-4 mt-12">
        {plans && plans.map((plan, index) => <Card plan={plan} key={index} />)}
      </div>
    </div>
  );
};

export default Page;

