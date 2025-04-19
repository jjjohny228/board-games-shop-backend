import { test, expect } from "@playwright/test";
import Env from "@helpers/env";

const baseUrl = Env.URL;

test.describe("Age Group", () => {
    // позитивні
    test("Get age group returns 200", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?age_group=1`);
        expect(response.status()).toBe(200);
    });
    test("GET two age groups returns 200", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?age_group=1&age_group=2`);
        expect(response.status()).toBe(200);
    });
    test("Get with empty age group returns 200", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?age_group=`);
        expect(response.status()).toBe(200);
    });
    // negative
    test("GET with string age group returns 400", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?age_group=abc`);
        expect(response.status()).toBe(400);
    });
    test("GET with negative number as age group returns 400", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?age_group=-1`);
        expect(response.status()).toBe(400);
    });
    test("Get with 0 age group returns 400", async ({ request }) => { 
        const response = await request.get(`${baseUrl}/api/games/?age_group=0`);
        expect(response.status()).toBe(400);
    });
});
test.describe("Difficulty", () => {
    // позитивні
    test("Get difficulty returns 200", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?difficulty=1`);
        expect(response.status()).toBe(200);
    });
    test("GET two difficulties returns 200", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?difficulty=1&difficulty=2`);
        expect(response.status()).toBe(200);
    });
    
    // негативні
    test("GET with string difficulty returns 400", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?difficulty=abc`);
        expect(response.status()).toBe(400);
    });
    test("GET with negative number as difficulty returns 400", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?difficulty=-1`);
        expect(response.status()).toBe(400);
    });
    test("Get with empty difficulty returns 200", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?difficulty=`);
        expect(response.status()).toBe(200);
    });
    test("Get with 0 difficulty returns 400", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?difficulty=0`);
        expect(response.status()).toBe(400);
    })
});
test.describe("Duration", () => {
    // позитивні
    test("Get duration returns 200", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?duration=1`);
        expect(response.status()).toBe(200);
    });
    test("GET two durations returns 200", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?duration=1&duration=2`);
        expect(response.status()).toBe(200);
    });
    test("Get with empty duration returns 200", async ({ request }) => {    
        const response = await request.get(`${baseUrl}/api/games/?duration=`);
        expect(response.status()).toBe(200);
    });
    // негативні
    test("GET with string duration returns 400", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?duration=abc`);
        expect(response.status()).toBe(400);
    });
    test("GET with negative number as duration returns 400", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?duration=-1`);
        expect(response.status()).toBe(400);
    });
    test("Get with 0 duration returns 400", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?duration=0`);
        expect(response.status()).toBe(400);
    });
});
test.describe("Genre", () => { 
    // позитивні
    test("Get genre returns 200", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?genre=1`);
        expect(response.status()).toBe(200);
    });
    test("GET two genres returns 200", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?genre=1&genre=2`);
        expect(response.status()).toBe(200);
    });
    test("Get with empty genre returns 200", async ({ request }) => {    
        const response = await request.get(`${baseUrl}/api/games/?genre=`);
        expect(response.status()).toBe(200);
    });
    // негативні
    test("GET with string genre returns 400", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?genre=abc`);
        expect(response.status()).toBe(400);
    });
    test("GET with negative number as genre returns 400", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?genre=-1`);
        expect(response.status()).toBe(400);
    });
    test("Get with 0 genre returns 400", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?genre=0`);
        expect(response.status()).toBe(400);
    })
})
test.describe("Player_count", () => {
    // позитивні
    test("Get player_count returns 200", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?player_count=1`);
        expect(response.status()).toBe(200);
    });
    test("GET two player_counts returns 200", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?player_count=1&player_count=2`);
        expect(response.status()).toBe(200);
    });
    test("Get with empty player_count returns 200", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?player_count=`);
        expect(response.status()).toBe(200);
    })
    // негативні
    test("GET with string player_count returns 400", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?player_count=abc`);
        expect(response.status()).toBe(400);
    });
    test("GET with negative number as player_count returns 400", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?player_count=-1`);
        expect(response.status()).toBe(400);
    });
    test("Get with 0 player_count returns 400", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?player_count=0`);
        expect(response.status()).toBe(400);
    })
});
test.describe("Mechanic", () => {
    // позитивні
    test("Get mechanic returns 200", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?mechanic=1`);
        expect(response.status()).toBe(200);
    });
    test("GET two mechanics returns 200", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?mechanic=1&mechanic=2`);
        expect(response.status()).toBe(200);
    });
    test("Get with empty mechanic returns 200", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?mechanic=`);
        expect(response.status()).toBe(200);
    });
    // негативні
    test("GET with string mechanic returns 400", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?mechanic=abc`);
        expect(response.status()).toBe(400);
    });
    test("GET with negative number as mechanic returns 400", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?mechanic=-1`);
        expect(response.status()).toBe(400);
    });
    test("Get with 0 mechanic returns 400", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?mechanic=0`);
        expect(response.status()).toBe(400);
    })
});
test.describe("Type", () => {
    // позитивні
    test("Get type returns 200", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?type=1`);
        expect(response.status()).toBe(200);
    });
    test("GET two types returns 200", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?type=1&type=2`);
        expect(response.status()).toBe(200);
    });
    test("Get with empty type returns 200", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?type=`);
        expect(response.status()).toBe(200);
    })
    // негативні
    test("GET with string type returns 400", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?type=abc`);
        expect(response.status()).toBe(400);
    });
    test("GET with negative number as type returns 400", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?type=-1`);
        expect(response.status()).toBe(400);
    });
    test("Get with 0 type returns 400", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?type=0`);
        expect(response.status()).toBe(400);
    });
});
test.describe("Price", () => {
    // позитивні
    test("GET with max_price=150 returns 200", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?max_price=500`);
        expect(response.status()).toBe(200);
    });
    test("GET with min_price=200 returns 200", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?min_price=200`);
        expect(response.status()).toBe(200);
    });
    test("GET with max_price=150 and min_price=200 returns 200", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?max_price=150&min_price=200`);
        expect(response.status()).toBe(200);
    });
    test("Get with empty max_price returns 200", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?max_price=`);
        expect(response.status()).toBe(200);
    });
    test("Get with empty min_price returns 200", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?min_price=`);
        expect(response.status()).toBe(200);
    })
    // негативні
    test("GET with string max_price returns 400", async ({ request }) => {
        const response2 = await request.get(`${baseUrl}/api/games/?max_price=abc`);
        expect(response2.status()).toBe(400);
    });
    test("GET with negative number as max_price returns 400", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?max_price=-1`);
        expect(response.status()).toBe(400);
        //! можливо проблема
    });
    test("GET with string min_price returns 400", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?min_price=abc`);
        expect(response.status()).toBe(400);
    });
    test("GET with negative number as min_price returns 400", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?min_price=-1`);
        expect(response.status()).toBe(400);
    });
    test("GET with min_price > max_price returns 400", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?min_price=200&max_price=100`);
        expect(response.status()).toBe(400);
    });
});
test.describe("Search", () => { 
    test("GET with string search returns 200", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?search=abc`);
        expect(response.status()).toBe(200);
    });
    test("GET with number search returns 200", async ({ request }) => { 
        const response = await request.get(`${baseUrl}/api/games/?search=1`);        
        expect(response.status()).toBe(200);
    })
})
test.describe("Sort", () => {
    // позитивні
    test("GET with sort=price returns 200", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?sort=price`);
        expect(response.status()).toBe(200);
    });
    test("GET with sort=-price returns 200", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?sort=-price`);
        expect(response.status()).toBe(200);
    });
    test("GET with sort=title returns 200", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?sort=title`);
        expect(response.status()).toBe(200);
    });
    test("GET with sort=-title returns 200", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?sort=-title`);
        expect(response.status()).toBe(200);
    });
    // негативні
    test("GET with sort=abc returns 400", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?sort=abc`);
        expect(response.status()).toBe(400);
    });
    test("GET with sort=-abc returns 400", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?sort=-abc`);
        expect(response.status()).toBe(400);
    });
})
test.describe("Some params", () => {
    test("GET with some params returns 200", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?search=abc&sort=title&min_price=100&max_price=200`);
        expect(response.status()).toBe(200);
    });
    test("GET with all params returns 200", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?age_group=2&difficulty=1&duration=3&genre=2&max_price=150&mechanic=2&min_price=100&player_count=3&type=2`);
        expect(response.status()).toBe(200);
    });
})