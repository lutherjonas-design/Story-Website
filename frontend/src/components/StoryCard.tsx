
import React from "react";
import { Link } from "react-router-dom"; // <— React Router
import "./StoryCard.css";

export type Story = {
  id: number | string;
  title: string;
  teaser?: string;
  author?: string;
  last_updated?: string;
  /** Optional image URL for the right panel */
  imageUrl?: string;
};

type Props = {
  story: Story;
  /** Optional override for default/fallback image */
  defaultImageUrl?: string;
  /** Compact variation */
  compact?: boolean;
  /** Remove hover elevation */
  flat?: boolean;
  /** Optional aria label override */
  ariaLabel?: string;
};

export default function StoryCard({
  story,
  defaultImageUrl = "/assets/placeholders/story-default.jpg",
  compact,
  flat,
  ariaLabel
}: Props) {
  const to = `/story/${encodeURIComponent(String(story.id))}`;

  const safeDate =
    story.last_updated ? new Date(story.last_updated) : undefined;
  const dateDisplay =
    safeDate && !isNaN(safeDate.getTime())
      ? safeDate.toLocaleDateString()
      : undefined;

  const image = story.imageUrl ?? defaultImageUrl ?? null;
  const hasTeaser = Boolean(story.teaser && story.teaser.trim().length > 0);

  return (
    <article
      className={[
        "story-card",
        compact ? "story-card--compact" : "",
        flat ? "story-card--flat" : ""
      ].join(" ")}
      aria-label={ariaLabel ?? story.title}
    >
      {/* Full-card Link (accessible & keyboard focusable) */}
      <Link
        className="story-card__link"
        to={to}
        aria-label={`Open story: ${story.title}`}
      />

      {/* Left / text */}
      <div className="story-card__content">
        <h3 className="story-card__title">{story.title}</h3>

        {/* Omit teaser entirely if not provided */}
        {hasTeaser && <p className="story-card__teaser">{story.teaser}</p>}

        <div className="story-card__meta">
          {story.author ? <>By {story.author}</> : null}
          {story.author && dateDisplay ? " • " : null}
          {dateDisplay ? <>{dateDisplay}</> : null}
        </div>
      </div>

      {/* Right / media (image or default) */}
      <div className="story-card__media" aria-hidden="true">
        {image ? (
          <img
            className="story-card__img"
            src={image}
            alt=""
            loading="lazy"
            decoding="async"
          />
        ) : (
          <div className="story-card__placeholder" />
        )}
      </div>
    </article>
  );
}