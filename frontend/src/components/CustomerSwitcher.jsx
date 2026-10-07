import React, { useState, useRef, useEffect } from "react";
import {
  CUSTOMER_PERSONAS,
  GUEST_CUSTOMER,
  GROUP_META,
  groupPersonas,
} from "../data/personas";

const GROUP_ORDER = ["trusted", "new", "suspicious", "review_offender", "edge"];

const COLOR_CLASSES = {
  gray: { dot: "bg-gray-400", pill: "bg-gray-100 text-gray-700" },
  emerald: { dot: "bg-emerald-500", pill: "bg-emerald-100 text-emerald-700" },
  blue: { dot: "bg-blue-500", pill: "bg-blue-100 text-blue-700" },
  red: { dot: "bg-red-500", pill: "bg-red-100 text-red-700" },
  amber: { dot: "bg-amber-500", pill: "bg-amber-100 text-amber-700" },
  purple: { dot: "bg-purple-500", pill: "bg-purple-100 text-purple-700" },
};

function CustomerSwitcher({ currentPersona, onSelect }) {
  const [open, setOpen] = useState(false);
  const wrapperRef = useRef(null);

  useEffect(() => {
    function handleClickOutside(e) {
      if (wrapperRef.current && !wrapperRef.current.contains(e.target)) {
        setOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const groups = groupPersonas();
  const currentColor = COLOR_CLASSES[GROUP_META[currentPersona.group].color];

  const handleSelect = (persona) => {
    onSelect(persona);
    setOpen(false);
  };

  return (
    <div className="relative" ref={wrapperRef}>
      <button
        onClick={() => setOpen((prev) => !prev)}
        className="flex items-center gap-2 px-3 py-2 rounded-lg border border-gray-300 bg-white hover:bg-gray-50 transition-colors text-sm"
      >
        <span className={`w-2 h-2 rounded-full ${currentColor.dot}`}></span>
        <span className="text-gray-500 text-xs">Shopping as</span>
        <span className="font-medium text-gray-900">
          {currentPersona.id === "guest" ? "Guest" : currentPersona.name}
        </span>
        <span className="text-gray-400 text-xs">v</span>
      </button>

      {open && (
        <div className="absolute right-0 mt-2 w-96 max-h-[520px] overflow-y-auto bg-white border border-gray-200 rounded-xl shadow-lg z-50">
          {/* Guest option */}
          <div className="p-2">
            <button
              onClick={() => handleSelect(GUEST_CUSTOMER)}
              className={`w-full text-left px-3 py-2 rounded-lg hover:bg-gray-50 transition-colors ${
                currentPersona.id === "guest" ? "bg-indigo-50" : ""
              }`}
            >
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-gray-400"></span>
                <span className="font-medium text-sm text-gray-900">
                  {GUEST_CUSTOMER.label}
                </span>
              </div>
              <p className="text-xs text-gray-500 mt-1 ml-4">
                {GUEST_CUSTOMER.hint}
              </p>
            </button>
          </div>

          {/* Grouped personas */}
          {GROUP_ORDER.map((groupKey) => {
            const personas = groups[groupKey];
            if (!personas || personas.length === 0) return null;

            const meta = GROUP_META[groupKey];
            const colors = COLOR_CLASSES[meta.color];

            return (
              <div key={groupKey} className="border-t border-gray-100">
                <div className="px-3 py-2 bg-gray-50">
                  <span
                    className={`text-[11px] font-semibold uppercase tracking-wide px-2 py-0.5 rounded ${colors.pill}`}
                  >
                    {meta.label}
                  </span>
                </div>
                <div className="p-2">
                  {personas.map((persona) => (
                    <button
                      key={persona.id}
                      onClick={() => handleSelect(persona)}
                      className={`w-full text-left px-3 py-2 rounded-lg hover:bg-gray-50 transition-colors ${
                        currentPersona.id === persona.id ? "bg-indigo-50" : ""
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <span
                            className={`w-2 h-2 rounded-full ${colors.dot}`}
                          ></span>
                          <span className="font-medium text-sm text-gray-900">
                            {persona.label}
                          </span>
                        </div>
                        <span className="text-[11px] text-gray-400">
                          {persona.location}
                        </span>
                      </div>
                      <p className="text-xs text-gray-500 mt-1 ml-4">
                        {persona.hint}
                      </p>
                    </button>
                  ))}
                </div>
              </div>
            );
          })}

          <div className="border-t border-gray-100 p-3 bg-gray-50 rounded-b-xl">
            <p className="text-[11px] text-gray-500 leading-relaxed">
              Selecting a persona auto fills checkout and review forms with
              their real name, phone, and address. The AI agent will see the
              full history tied to that identity.
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

export default CustomerSwitcher;
