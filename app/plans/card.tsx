import React, { useState } from "react";
import { plans } from "./page";
interface cardProps {
  plan: plans;
}
const Card: React.FC<cardProps> = ({ plan }) => {
  return (
    <div className=" border-gray-200 border hover:shadow-lg hover:shadow-gray-300 p-4 rounded-lg">
      {plan.list_of_items.map((item: any, index) => (
        <div className="flex items-center space-x-4" key={index}>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-gray-900 truncate ">
              {item.title}
            </p>
            <p className="text-sm text-gray-500 truncate ">{item.price}</p>
          </div>
        </div>
      ))}
      <div className="text-center text-gray-900 m-6">
        <label className="font-bold text-lg">$</label>{" "}
        <label className="font-semibold">{plan.cost.total_cost}</label>
      </div>
    </div>
  );
};
export default Card;
