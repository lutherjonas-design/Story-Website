import { Chapter } from '../types/chapter'
import { Link } from "react-router-dom";

import './ChapterCard.css'

interface Props {
  chapter: Chapter;
  slug?: string;
};

export default function({ chapter, slug }: Props){
    
    return (
    <Link
      to={`/s/${slug}/${chapter.order}`}
      state={{ chapter }}                // pass cached data to avoid a refetch
      className="chaptercard__link"
    >
      <article className="chaptercard">
        <div className="chaptercard__content">
          <h3 className="chaptercard__title">{chapter.order}: {chapter.title}</h3>
        </div>
      </article>
    </Link>
  );
}