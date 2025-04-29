import { test, expect } from "@playwright/test";
import Env from "@helpers/env";

const baseUrl = Env.URL;
const param = ["age_group", "difficulty", "duration", "genre", "mechanic", "player_count", "type"];

test("No params returns 200", async ({ request }) => {
    const response = await request.get(`${baseUrl}/api/games/`);
    expect(response.status()).toBe(200);
});
for (let p of param) {
    test.describe(`Check params`, () => {
        // positive
        test(`Get ${p} returns 200`, async ({ request }) => {
            const response = await request.get(`${baseUrl}/api/games/?${p}=1`);
            expect(response.status()).toBe(200);
        });
        test(`GET two ${p} returns 200`, async ({ request }) => {
            const response = await request.get(`${baseUrl}/api/games/?${p}=1&${p}=2`);
            expect(response.status()).toBe(200);
        });
        test(`Get with empty ${p} returns 200`, async ({ request }) => {
            const response = await request.get(`${baseUrl}/api/games/?${p}=`);
            expect(response.status()).toBe(200);
        });
        test(`Get with multiple ${p} returns 200`, async ({ request }) => {
            const response = await request.get(`${baseUrl}/api/games/?${p}=1&${p}=2&${p}=3`);
            expect(response.status()).toBe(200);
        })
        test(`Get ${p} returns valid json`, async ({ request }) => {
            const response = await request.get(`${baseUrl}/api/games/?${p}=1`);
            const json = await response.json();
            expect(json).toBeTruthy();
        });
        // negative
        test(`GET with string ${p} returns 400`, async ({ request }) => {
            const response = await request.get(`${baseUrl}/api/games/?${p}=abc`);
            expect(response.status()).toBe(400);
        });
        test(`GET with negative number as ${p} returns 400`, async ({ request }) => {
            const response = await request.get(`${baseUrl}/api/games/?${p}=-1`);
            expect(response.status()).toBe(400);
        });
        test(`Get with 0 ${p} returns 400`, async ({ request }) => {
            const response = await request.get(`${baseUrl}/api/games/?${p}=0`);
            expect(response.status()).toBe(400);
        });
        test(`Get with 1000 ${p} id returns 400`, async ({ request }) => {
            const response = await request.get(`${baseUrl}/api/games/?${p}=1000`);
            expect(response.status()).toBe(400);
        });
    });
};
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
    test("GET with max_price=150 and min_price=200 returns 400", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?max_price=150&min_price=200`);
        expect(response.status()).toBe(400);
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
        //! можливо не проблема
    });
    test("GET with string min_price returns 400", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?min_price=abc`);
        expect(response.status()).toBe(400);
    });
    test("GET with negative number as min_price returns 400", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?min_price=-1`);
        expect(response.status()).toBe(400);
        //! можливо не проблема
    });
    test("GET with min_price > max_price returns 400", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?min_price=200&max_price=100`);
        expect(response.status()).toBe(400);
    });
    test("Get with max_price=min_price returns 200", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?min_price=200&max_price=200`);
        expect(response.status()).toBe(200);
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
});
test.describe("Some params", () => {
    test("GET with some params returns 200", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?search=abc&sort=title&min_price=100&max_price=200`);
        expect(response.status()).toBe(200);
    });
    test("GET with all params returns 200", async ({ request }) => {
        const response = await request.get(`${baseUrl}/api/games/?age_group=2&difficulty=1&duration=3&genre=2&max_price=150&mechanic=2&min_price=100&player_count=3&type=2`);
        expect(response.status()).toBe(200);
    });
});