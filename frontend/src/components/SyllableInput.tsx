import { useRef } from "react";
import '@/components/SyllableInput.css'

export type Status= "valid" | "invalid" | "not_found" | "normal"
  
const statusClassMap: Record<Status, string> = {
  valid: "SyllableInput-valid",
  invalid: "SyllableInput-invalid",
  not_found: "SyllableInput-not_found",
  normal: ""
};

type Props = {
  value: string[];
  onChange: (value: string[]) => void;
  onSubmit?: () => void;
  status?:Status
};

export function SyllableInput({ value, onChange, onSubmit, status }: Props) {
  const fields = [...value, ""];
  const inputRefs = useRef<HTMLInputElement[]>([]);
  inputRefs.current.length = fields.length; // keep refs array in sync

  return (
    <div className={`SyllableInput ${status?statusClassMap[status]:""}`}>
      {fields.map((v, i) => (
        <input
          className="SyllableInputField"
          size={Math.max(1, (v?.length ?? 0))}
          key={i}
          value={v}
          ref={(el) => {
            if (el) inputRefs.current[i] = el;
          }}
          onKeyDown={(e) => {
            const el = e.currentTarget; // the current <input>
            const caretStart = el.selectionStart ?? 0;
            const caretEnd = el.selectionEnd ?? 0;
            const currVal = value[i] ?? ""; // safe even for trailing ("")
            // --- Enter: Submit
            if (e.key === "Enter") {
              e.preventDefault();
              onSubmit?.();
            }
            // --- ArrowLeft: jump to previous if at the start ---
            if (e.key === "ArrowLeft" && caretStart === 0 && caretEnd === 0) {
              e.preventDefault();
              const prevEl = inputRefs.current[i - 1];
              if (prevEl) {
                prevEl.focus();
                // put caret at end of previous input
                requestAnimationFrame(() => {
                  const len = (value[i - 1]?.length ?? 0);
                  prevEl.setSelectionRange(len, len);
                });
              }
              return;
            }
            // --- ArrowRight: jump to next if at the end ---
            if (e.key === "ArrowRight" && caretStart === currVal.length && caretEnd === currVal.length) {
              e.preventDefault();
              const nextEl = inputRefs.current[i + 1];
              if (nextEl) {
                nextEl.focus();
                // put caret at start of next input
                requestAnimationFrame(() => {
                  nextEl.setSelectionRange(0, 0);
                });
              }
              return;
            }
            // --- Backspace: basically a jump on empty, since onChange deletes empty ---
            if (e.key === "Backspace" && caretStart === 0 && caretEnd === 0) {
              if (currVal === "") {
                e.preventDefault();

                // If it's a real slot (not the trailing empty at the far right), remove it
                if (i < value.length) {
                  const next = [...value];
                  // Remove the current empty field
                  next.splice(i, 1);
                  onChange(next);
                }

                // Focus the previous input (if any) and put caret at end
                const prevEl = inputRefs.current[i - 1];
                if (prevEl) {
                  prevEl.focus();
                  requestAnimationFrame(() => {
                    const len = (value[i - 1]?.length ?? 0);
                    prevEl.setSelectionRange(len, len);
                  });
                }
                return;
              }
              // If currVal is not empty and caret at start, you might want to merge with previous later.
            }
            // Handle Shift+Tab (go back)
            if (e.key === "Tab" && e.shiftKey) {
              e.preventDefault();
              inputRefs.current[i - 1]?.focus();
              return;
            }
            // Handle Space or Tab (go forward)
            if (e.key === " " || e.key === "Tab") {
              e.preventDefault();
              inputRefs.current[i + 1]?.focus(); //? is like an if check
            }
          }}

          onChange={(e) => {
            const next = [...value];
            const newVal = e.target.value;

            if (i < value.length) {
              next[i] = newVal;
            } else {
              if (newVal !== "") next.push(newVal);
            }

            // Remove only a trailing empty we might have accidentally created
            const normalized =
              next.length > 0 && next[next.length - 1] === ""
                ? next.slice(0, -1)
                : next;

            onChange(normalized);
          }}
        />
      ))}
    </div>
  );
}