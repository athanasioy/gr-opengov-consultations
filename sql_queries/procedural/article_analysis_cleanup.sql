/* DELETE Matchings for Unable to Match Legislations */
UPDATE Article
SET voted_article_id = NULL
WHERE
legislation_id in (629, 473, 505, 182, 845, 439,
151, 299, 541, 655, 144, 340, 561, 250, 356,
589, 552, 503, 832, 239, 254, 621, 249, 271,
214, 536, 620, 758, 230, 216, 121, 370, 622,
759, 323, 594, 369, 847, 587, 837, 527, 314,
260, 317, 646, 382, 241, 486, 625, 437, 812,
480, 848, 248, 347, 387, 431, 227, 372, 402,
369, 160, 529);

/* DELETE Matchings were similarity is below 0.05 (is assumed to be wrong) */
UPDATE Article
SET voted_article_id = NULL
WHERE id in (SELECT p_articleID FROM ArticleAnalysis WHERE similarity_ratio < 0.05);


/* DELETE Specifics Matcings Manually */
UPDATE Article 
SET voted_article_id = NULL
WHERE
legislation_id = 183
and cast(number as integer) > 25;

UPDATE Article 
SET voted_article_id = NULL
WHERE
legislation_id = 835
and cast(number as integer) > 15;

--	403 very nice (DROP AFTER 35>)
UPDATE Article 
SET voted_article_id = NULL
WHERE
legislation_id = 403
and cast(number as integer) > 35;

-- 442 very nice (DROP AFTER 55>)
UPDATE Article 
SET voted_article_id = NULL
WHERE
legislation_id = 442
and cast(number as integer) > 55;

-- 247 very nice (Drop after 12>)
UPDATE Article 
SET voted_article_id = NULL
WHERE
legislation_id = 247
and cast(number as integer) > 12;

-- 410 very nice (DROP AFTER 24>)
UPDATE Article 
SET voted_article_id = NULL
WHERE
legislation_id = 410
and cast(number as integer) > 24;

-- 253 is mostly correct (4<x<18)
UPDATE Article 
SET voted_article_id = NULL
WHERE
legislation_id = 253
and (cast(number as integer) > 18 or cast(number as integer)< 4);


-- 506 is good (KEEP ONLY 01)
UPDATE Article 
SET voted_article_id = NULL
WHERE
legislation_id = 506
and cast(number as integer) > 1;

-- 109 is good (drop after 19>)
UPDATE Article 
SET voted_article_id = NULL
WHERE
legislation_id = 109
and cast(number as integer) > 19;

-- 	484 is good (keep after 15>)
UPDATE Article 
SET voted_article_id = NULL
WHERE
legislation_id = 484
and cast(number as integer) > 15;

-- 64 mostly correct (after 13>)
UPDATE Article 
SET voted_article_id = NULL
WHERE
legislation_id = 64
and cast(number as integer) > 13;

-- 548 is good (DROP after 50>)
UPDATE Article 
SET voted_article_id = NULL
WHERE
legislation_id = 548
and cast(number as integer) > 50;

-- 	749 is good (Drop After 10>)
UPDATE Article 
SET voted_article_id = NULL
WHERE
legislation_id = 749
and cast(number as integer) > 10;

-- 	141 is good (drop 38,39)
UPDATE Article 
SET voted_article_id = NULL
WHERE
legislation_id = 141
and (cast(number as integer) = 39 or cast(number as integer) = 38);

-- 623 is good (KEEP x<=24 and x>=45)
UPDATE Article 
SET voted_article_id = NULL
WHERE
legislation_id = 623
and cast(number as integer) >25  and cast(number as integer) <45;

-- 295 is good (keep only 01)
UPDATE Article 
SET voted_article_id = NULL
WHERE
legislation_id = 295
and cast(number as integer) > 1;

-- 97 is good (drop after 55>)
UPDATE Article 
SET voted_article_id = NULL
WHERE
legislation_id = 97
and cast(number as integer) >55;

-- 139 is good (drop after 26>)
UPDATE Article 
SET voted_article_id = NULL
WHERE
legislation_id = 139
and cast(number as integer) >26;

-- 	108 is good (keep 1 only)
UPDATE Article 
SET voted_article_id = NULL
WHERE
legislation_id = 108
and cast(number as integer) >1;

-- 122 is good ( drop 8)
UPDATE Article 
SET voted_article_id = NULL
WHERE
legislation_id = 122
and cast(number as integer) =8;

-- 59 is good (drop 21)
UPDATE Article 
SET voted_article_id = NULL
WHERE
legislation_id = 59
and cast(number as integer) = 21;

-- 574 is good (drop 8)
UPDATE Article 
SET voted_article_id = NULL
WHERE
legislation_id = 574
and cast(number as integer) = 8;

-- 123 is good (drop before 12<)
UPDATE Article 
SET voted_article_id = NULL
WHERE
legislation_id = 123
and cast(number as integer) < 12;

-- 147 is good (drop 40)
UPDATE Article 
SET voted_article_id = NULL
WHERE
legislation_id = 147
and cast(number as integer) = 40;

-- 114 is good (drop 1 & 166)
UPDATE Article 
SET voted_article_id = NULL
WHERE
legislation_id = 114
and (cast(number as integer) = 1 or cast(number as integer) = 166);

-- 198 is good (drop 8)
UPDATE Article 
SET voted_article_id = NULL
WHERE
legislation_id = 198
and cast(number as integer) = 8;

-- 119 is good (drop 15>)
UPDATE Article 
SET voted_article_id = NULL
WHERE
legislation_id = 119
and cast(number as integer) > 15;

-- 363 is good (drop 15)
UPDATE Article 
SET voted_article_id = NULL
WHERE
legislation_id = 363
and cast(number as integer) = 15;

-- 126 is good (drop 08)
UPDATE Article 
SET voted_article_id = NULL
WHERE
legislation_id = 126
and cast(number as integer) = 8;

-- 358 is good (drop after 07>)
UPDATE Article 
SET voted_article_id = NULL
WHERE
legislation_id = 358
and cast(number as integer) > 7;

-- 448 is good (drop 58)
UPDATE Article 
SET voted_article_id = NULL
WHERE
legislation_id = 448
and cast(number as integer) = 58;

-- 187 is good (drop 32)
UPDATE Article 
SET voted_article_id = NULL
WHERE
legislation_id = 187
and cast(number as integer) = 32;

-- 52 is good (drop 34 & 50)
UPDATE Article 
SET voted_article_id = NULL
WHERE
legislation_id = 52
and (cast(number as integer) = 34 or cast(number as integer) = 50);

--788 is correct mostly (drop before 23<)
UPDATE Article 
SET voted_article_id = NULL
WHERE
legislation_id = 788
and cast(number as integer) < 23;


/* Delete Matchings where multiple articles matched to same voted Article (Keep Max)*/
UPDATE Article
SET voted_article_id = NULL
WHERE id in (
	SELECT A.p_articleID FROM (
		SELECT 	p_legislation_id,
				p_articleID,
				p_articleNo,
				f_articleID,
				f_articleNo,
				similarity_ratio,
				CASE WHEN max(similarity_ratio) OVER (PARTITION BY f_articleID) <> similarity_ratio THEN 1 ELSE 0 END as ShouldBeDeleted,
				max(similarity_ratio) OVER (PARTITION BY f_articleID) as MaxSimilarityPerMappedArticle
		from ArticleAnalysis
		--where ArticleAnalysis.f_articleID in ( SELECT f_articleID FROM ArticleAnalysis group by f_articleID having count(*)>1)
		where f_articleID IS NOT NULL
		--order by cast(f_articleID as integer), p_legislation_id
	) AS A
	WHERE A.ShouldBeDeleted=1
);

/*
select f_articleID, count(DISTINCT p_legislation_id) from ArticleAnalysis
group by f_articleID
having count(DISTINCT p_legislation_id) >1
*/
/*DELETE Failed Matches */
DELETE FROM ArticleAnalysis where f_articleID IS NULL;

/* DELETE Mathings where the ArticleNo is not specified */
DELETE FROM ArticleAnalysis WHERE p_articleNo = 999;

/* DELETE ArticleAnalysis where the matching was explicitly set to NULL */
DELETE FROM ArticleAnalysis
WHERE p_articleID in (SELECT id FROM Article WHERE voted_article_id IS NULL);

/* DELETE ArticleAnalysis rows were both proposed text and voted text is empty*/
DELETE FROM ArticleAnalysis
WHERE similarity_ratio=1
