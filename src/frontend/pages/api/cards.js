import { connectToDatabase } from "../../util/mongodb";

export default async (req, res) => {
  // Build the query object from the request parameters
  let conditions = {};
  let clauses = [];
  if(req.query.multiverseid) clauses.push({ multiverseid: req.query.multiverseid });
  if(req.query.name) clauses.push({ name: {$regex : ".*" + req.query.name+ ".*"} });
  if(req.query.artist) clauses.push({ name: {$regex : ".*" + req.query.artist + ".*"} });

  // Make sure no $and clause is included if no parameters were given
  // else, clauses is empty and conditions = {] is used
  if(clauses.length > 0) conditions['$and'] = clauses;

  console.log("Conditions:");
  console.log(conditions)
  console.log("Clauses:");
  console.log(clauses)

  const { db } = await connectToDatabase();

  const cards = await db
    .collection("Cards")
    .find(conditions)
    .limit(100)
    .toArray();

  res.json(cards);

};