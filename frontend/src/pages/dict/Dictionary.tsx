import { useState, useEffect } from 'react'
import { useCandidates } from '@/hooks/useCandidates'
import { useTransfer } from '@/hooks/useTransfer'

import { SyllableInput } from '@/components/SyllableInput'

import { Word } from '@/types/word'
import { Status } from '@/components/SyllableInput'

import { validateSyllables } from '@/utils/validateSyllables'



type Prop = {
  word?: Word
}

function isSameWord(a: Word, b: Word) {
  return a.id === b.id;
}

export default function Transfer(props: Prop) {
  const [syllables, setSyllables] = useState<string[] | []>([]);
  const [status, setStatus] = useState<Status>("normal");
  const [wordPair, setPair] = useState<{ current: Word | null; next: Word | null }>({
    current: null,
    next: null,
  });

  const { words, loading, error } = useCandidates({ limit: 2 });
  const { loading: sendLoad, error:sendError, lastStatus:sendLastStatus, send } = useTransfer();

  useEffect(() => {
    if (!words || words.length < 2) return;

    const [first, second] = words;

    if (props.word) {
      // prefill rule with id comparison
      if (isSameWord(first, props.word)) {
        setPair({ current: first, next: second });
      } else {
        setPair({ current: props.word, next: second });
      }
    } else {
      setPair({ current: first, next: second });
    }
    // We intentionally ignore loading/error for now (no edge cases yet)
  }, [words, props.word]);

  const handleSubmit = async () => {
    // Parent normalizes the data
    console.log(syllables);
    const cleaned = syllables.map(s => s.toLowerCase()).filter(Boolean);
    if (syllables.length==0){
      setStatus("normal")
    } else if (wordPair.current?.word && validateSyllables(wordPair.current.word, syllables)){
      const result = await send({ id:wordPair.current?.id, word:wordPair.current?.word, syllables });
      setStatus("valid");
      console.log("valid");
    } else {
      setStatus("invalid");
    }
    console.log("SUBMITTED:", cleaned);
    // Example: call an API, validate, etc.
    // submitSyllables(cleaned)
  };


  return (
    <main>
      <h1>Transfer</h1>
      <div>
        <div>{wordPair.current ? wordPair.current.word : "—"}</div>
        <SyllableInput 
          value={syllables} 
          onChange = {setSyllables}
          onSubmit={handleSubmit}
          status={status}
        />
      </div>

    </main>
  )
}
