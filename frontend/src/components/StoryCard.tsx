import { Link } from "react-router-dom";

import { Story } from "../types/story";
import { timeAgo } from "../utils/Dates";

import "./StoryCard.css";

type Props = {
  story: Story;
};

export function StoryCard({ story }: Props) {
  return (
    <Link
      to={`/s/${story.slug}`}
      state={{ story }}                // pass cached data to avoid a refetch
      className="storycard__link"
    >
      <article className="storycard">
        <div className="storycard__content">
          <h3 className="storycard__title">{story.title}</h3>
          <p className="storycard__teaser">{story.teaser}</p>
          <p className="storycard__footer">
            {story.author} • {story.last_updated && timeAgo(story.last_updated)}
          </p>
        </div>
        <div className="storycard__image" />
      </article>
    </Link>
  );
}
