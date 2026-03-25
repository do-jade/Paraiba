import Comment from "../models/Comment.js";
import { ApifyClient } from "apify-client";

// helper to protect against deleted comments
function isDeletedComment(c) {
  const body = (c?.body ?? "").trim().toLowerCase();
  return body === "[deleted]" || body === "[removed]" || body === "";
}

export async function createCommentsUsingRedditScrapper(req, res) {
  try {
    const APIFY_TOKEN = process.env.APIFY_TOKEN;
    if (!APIFY_TOKEN) {
      return res
        .status(500)
        .json({ message: "Missing APIFY_TOKEN in environment" });
    }

    const client = new ApifyClient({
      token: APIFY_TOKEN,
    });

    // Prepare Actor input
    const input = {
      ignorestartUrls: false,
      includeNSFW: false,
      maxItems: 20,
      searchComments: true,
      searchCommunities: false,
      searchPosts: false,
      searchUsers: false,
      skipComments: false,
      skipCommunity: false,
      skipUserPosts: false,
      sort: "top",
      startUrls: [
        // {
        //   url: "https://www.reddit.com/r/GNV/comments/dydpd0/whats_the_most_underrated_restaurant_in_town/",
        // },
        // {
        //   url: "https://www.reddit.com/r/GNV/comments/1ixxyzg/best_new_or_hidden_gem_restaurants/",
        // },
        // {
        //   url: "https://www.reddit.com/r/GNV/comments/1jog9o7/best_hidden_resturant_gems_of_gainesville/",
        // },
        // {
        //   url: "https://www.reddit.com/r/GNV/comments/1ky80ob/hidden_gems_to_go_to_for_a_meal/",
        // },
        // {
        //   url: "https://www.reddit.com/r/GNV/comments/bi861b/hidden_food_gems/",
        // },
        // {
        //   url: "https://www.reddit.com/r/GNV/comments/ajenmt/anyone_know_any_outdoor_hidden_gems/",
        // },
        // {
        //   url: "https://www.reddit.com/r/GNV/comments/171j93p/fun_hidden_gems_in_gnv_that_are_cheapfree/",
        // },
        // {
        //   url: "https://www.reddit.com/r/GNV/comments/26zn3r/what_are_some_holeinthewallhidden_restaurant_gems/",
        // },
        // {
        //   url: "https://www.reddit.com/r/GNV/comments/7ozzn3/what_are_some_undiscovered_hidden_gem_restaurants/",
        // },
        // {
        //   url: "https://www.reddit.com/r/GNV/comments/14g7yv0/food_bucket_list_for_gnv/"
        // },
        // {
        //   url: "https://www.reddit.com/r/GNV/comments/s3gfeq/unique_restaurants_to_visit/"
        // },
        // {
        //   url: "https://www.reddit.com/r/GNV/comments/st75b7/i_just_got_a_new_job_and_i_want_to_go_somewhere/"
        // },
        // {
        //   url: "https://www.reddit.com/r/GNV/comments/16utspe/nice_restaurants_that_wont_break_the_bank/"
        // },
        // {
        //   url: "https://www.reddit.com/r/GNV/comments/1ax8txp/beautiful_outdoor_space/"
        // },
        // {
        //   url: "https://www.reddit.com/r/GNV/comments/uazmep/best_outdoor_date_ideas/"
        // },
        // {
        //   url: "https://www.reddit.com/r/GNV/comments/1p55ts9/best_nature_spot_to_chill/"
        // },
        // {
        //   url: "https://www.reddit.com/r/GNV/comments/1gagdh2/go_to_restaurants/"
        // },
        // {
        //   url: "https://www.reddit.com/r/GNV/comments/1kpyk74/best_sweet_treat_spot/"
        // },
        // {
        //   url: "https://www.reddit.com/r/GNV/comments/1ble1q8/best_dessert_in_gnv/"
        // }
        // {
        //   url: "https://www.reddit.com/r/GNV/comments/1pmejgt/favorite_local_experienceattraction/"
        // },
        // {
        //   url: "https://www.reddit.com/r/GNV/comments/7r378z/visiting_gainesville_for_a_week_what_should_i_do/"
        // }
        // {
        //   url: "https://www.reddit.com/r/GNV/comments/12xxhug/best_chinese_takeout_that_has_a_good_price_to/"
        // },
        // {
        //   url: "https://www.reddit.com/r/GNV/comments/1dbym7x/i_am_a_lone_traveler_and_im_very_bored_what/"
        // },
        // {
        //   url: "https://www.reddit.com/r/GNV/comments/1etmfsi/ideas_for_fun_things_to_do_in_gainesville_that/"
        // }

      ],
      time: "all",
    };

    // Run the Actor and wait for it to finish
    const run = await client
      .actor("practicaltools/apify-reddit-api")
      .call(input);

    // Fetch and print Actor results from the run's dataset (if any)
    console.log("Results from dataset");
    console.log(
      `💾 Check your data here: https://console.apify.com/storage/datasets/${run.defaultDatasetId}`,
    );
    const { items } = await client.dataset(run.defaultDatasetId).listItems();
    items.forEach((item) => {
      console.dir(item);
    });

    // ADD: store ONLY the comments in MongoDB
    const commentDocs = [];
    for (const item of items) {
      const comments = Array.isArray(item?.comments) ? item.comments : [];
      for (const c of comments) {
        if (isDeletedComment(c)) continue; // calls helper to protect against deleted comments
        commentDocs.push({
          comment_text: c?.body ?? "",
          upvotes: c?.upVotes ?? 0,
          link: c?.url ?? "",
        });
      }
    }

    if (commentDocs.length > 0) {
      // If you have a unique index on `link` you can switch to upsert logic later.
      await Comment.insertMany(commentDocs, { ordered: false });
    }

    console.log(`Inserted ${commentDocs.length} comments into DB`);

    return res.status(200).json({
      message: "Scrape complete",
      insertedCount: commentDocs.length,
    });
  } catch (error) {
    console.log("Error in createCommentsUsingRedditScrapper controller", error);
  }
}
