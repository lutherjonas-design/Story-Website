import { useCallback, useState } from "react";
import { validateSyllables } from "../utils/validateSyllables";

type TransferInput = {
    id: number;
    syllables: string[];
    word?: string;
};

type TransferResult =
    | "valid"
    | "invalid"
    | "not_found"
    | "error"
    | "invalid_local";

export function useTransfer() {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [lastStatus, setLastStatus] = useState<TransferResult | null>(null);

    const send = useCallback(async ({ id, word, syllables }: TransferInput): Promise<TransferResult> => {
        if (word && !validateSyllables(word, syllables)) {
            setLastStatus("invalid_local");
            return "invalid_local";
        }

        const controller = new AbortController();
        try {
            setLoading(true);
            setError(null);

            const res = await fetch("/api/dict/transfer/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                signal: controller.signal,
                body: JSON.stringify({ id, syllables })
            });

            // Map raw HTTP codes to our front-end friendly states:
            if (res.ok) {
                setLastStatus("valid");
                return "valid";
            }

            if (res.status === 404) {
                setLastStatus("not_found");
                return "not_found";
            }

            if (res.status === 400) {
                setLastStatus("invalid");
                return "invalid";
            }

            setLastStatus("error");
            setError(`Unexpected server error: ${res.status}`);
            return "error";

        } catch (err) {
            if (err instanceof DOMException && err.name === "AbortError") {
                // Abort → treat as neutral (user navigated away etc.)
                return "error";
            }

            setError((err as Error).message);
            setLastStatus("error");
            return "error";
        } finally {
            setLoading(false);
        }
    }, []);

    return { loading, error, lastStatus, send };
}