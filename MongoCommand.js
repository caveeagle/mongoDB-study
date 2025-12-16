
/* ************************************************ */

// Count how many books belong to the "Romance" genre
db.books.countDocuments({ genres: "Romance" })  // 53

// Find books by a specific author
db.books.find({ "authors.author_name": "Jojo Moyes" })  // All fields

// Putput only the selected fields:
db.books.find(
  { "authors.author_name": "Jojo Moyes" },
  {
    _id: 0,
    book_title: 1,
    authors: 1
  }
)

/* ************************************************ */


// Calculate the average rating for each book
// $avg can be applied directly to an array field
db.books.aggregate([
  {
    $project: {
      _id: 0,
      book_id: 1,
      book_title: 1,
      average_rating: { $avg: "$ratings" }
    }
  }
])

// Return top 10 books by average rating
db.books.aggregate([
  {
    $project: {
      _id: 0,
      book_title: 1,
      average_rating: { $avg: "$ratings" }
    }
  },
  {
    $sort: {
      average_rating: -1
    }
  },
  {
    $limit: 10
  }
])

/* ************************************************ */

// Plain List of books:
db.books.aggregate([
  {
    // Compute average rating per book
    $project: {
      book_title: 1,
      average_rating: { $avg: "$ratings" }
    }
  },
  {
    // Sort by average rating (highest first)
    $sort: {
      average_rating: -1
    }
  },
  {
    // Take top 10 books
    $limit: 10
  },
  {
    // Group titles into a single array !
    $group: {
      _id: null,
      titles: { $push: "$book_title" }
    }
  },
  {
    // Final projection: remove _id
    $project: {
      _id: 0,
      titles: 1
    }
  }
])

/* ************************************************ */

// Count how many books exist for each genre
// $unwind deconstructs the genres array
db.books.aggregate([
  {
    $unwind: "$genres"
  },
  {
    $group: {
      _id: "$genres",
      book_count: { $sum: 1 }
    }
  },
  {
    $sort: { book_count: -1 }
  }
])


// Determine how often each author appears across all books
// $unwind expands the authors array
db.books.aggregate([
  {
    $unwind: "$authors"
  },
  {
    $group: {
      _id: "$authors.author_name",
      book_count: { $sum: 1 }
    }
  },
  {
    $sort: { book_count: -1 }
  }
])

/* ************************************************ */
/* ************************************************ */
/* ************************************************ */

// Add the field "average_rating" rounded to 2 decimal places
db.books.updateMany(
  {},
  [
    {
      $set: {
        average_rating: {
          // $round rounds the value to the specified number of decimal places
          $round: [
            { $avg: "$ratings" }, 2
          ]
        }
      }
    }
  ]
)

/* ************************************************ */

// Create an index on the average_rating field
// This enables fast sorting and range queries by rating
db.books.createIndex(
  { average_rating: -1 }
)

// Check:
db.books.getIndexes()


// Find top 10 highest-rated books using the index
db.books.find(
  {},
  { _id: 0, book_title: 1, average_rating: 1 }
) .sort({ average_rating: -1 }) .limit(10)


/* ************************************************ */

// Count how many books have an average rating greater than 4.5
db.books.countDocuments({
  average_rating: { $gt: 4.6 }   // 15
})

// Find titles of books with average rating greater than 4.5
db.books.find(
  { average_rating: { $gt: 4.6 } },
  { _id: 0, book_title: 1 }
)
.sort({ average_rating: -1 })

/* ************************************************ */
/* ************************************************ */
/* ************************************************ */

/*   -==  Aggregation: most borrowed authors  ==-   */

// Determine the most borrowed authors based on total borrow events
db.books.aggregate([
  {
    // Expand authors array so each author is processed separately
    $unwind: "$authors"
  },
  {
    // Expand borrowers array to count each borrow event
    $unwind: "$borrowers"
  },
  {
    // Group by author name and count borrow events
    $group: {
      _id: "$authors.author_name",
      total_borrows: { $sum: 1 }
    }
  },
  {
    // Sort authors by number of borrows (descending)
    $sort: {
      total_borrows: -1
    }
  }
])

/* ************************************************ */

