extern crate poker_log_parser;
use poker_log_parser::simd::NameCacheSimd;

use criterion::{black_box, criterion_group, criterion_main, Criterion};

struct NameCache {
    data: [u8; 30],
    count: u8,
    stride: u8,
}

impl NameCache {
    fn new(stride: u8) -> Self {
        assert!(stride >= 1);
        assert!(stride <= 3);
        Self{data: [0; 30], count: 0, stride}
    }

    fn add(&mut self, name: &str) {
        assert!(name.len() >= self.stride as usize);
        let begin = self.count as usize * self.stride as usize;
        self.data[begin..begin + self.stride as usize].copy_from_slice(name[..self.stride as usize].as_bytes());
        self.count += 1;
    }

    fn slice<'a>(&'a self, i: u8) -> &'a str {
        let begin = i as usize * self.stride as usize;
        unsafe { std::str::from_utf8_unchecked(&self.data[begin..begin + self.stride as usize]) }
    }

    fn find(&self, s: &str) -> u8 {
        for i in 0..self.count {
            if s.starts_with(self.slice(i)) {
                return i;
            }
        }
        32 / self.stride * self.stride
    }
}
/*
NameCache (len=4, stride=3) - find success: index 0/4
                        time:   [4.0260 ns 4.1703 ns 4.3379 ns]

NameCache (len=4, stride=3) - find success: index 2/4
                        time:   [9.7076 ns 10.111 ns 10.535 ns]

NameCache (len=4, stride=3) - find success: index 3/4
                        time:   [12.177 ns 12.635 ns 13.123 ns]

NameCache (len=4, stride=3) - find fail
                        time:   [12.109 ns 12.524 ns 12.981 ns]

NameCache (len=10, stride=3) - find success: index 0/10
                        time:   [3.9973 ns 4.1443 ns 4.3069 ns]

NameCache (len=10, stride=3) - find success: index 5/10
                        time:   [16.378 ns 16.862 ns 17.410 ns]

NameCache (len=10, stride=3) - find success: index 9/10
                        time:   [26.998 ns 28.014 ns 29.139 ns]

NameCache (len=10, stride=3) - find fail
                        time:   [29.900 ns 31.119 ns 32.377 ns]

*/

/*
NameCacheSimd (len=4, stride=3) - find success: index 0/4
                        time:   [3.1930 ns 3.1946 ns 3.1964 ns]

NameCacheSimd (len=4, stride=3) - find success: index 2/4
                        time:   [3.2178 ns 3.2740 ns 3.3490 ns]

NameCacheSimd (len=4, stride=3) - find success: index 3/4
                        time:   [3.2015 ns 3.2386 ns 3.2934 ns]

NameCacheSimd (len=4, stride=3) - find fail
                        time:   [3.0972 ns 3.1086 ns 3.1245 ns]

NameCacheSimd (len=10, stride=3) - find success: index 0/10
                        time:   [3.1941 ns 3.2001 ns 3.2081 ns]

NameCacheSimd (len=10, stride=3) - find success: index 5/10
                        time:   [3.1979 ns 3.2065 ns 3.2188 ns]

NameCacheSimd (len=10, stride=3) - find success: index 9/10
                        time:   [3.1957 ns 3.2224 ns 3.2610 ns]

NameCacheSimd (len=10, stride=3) - find fail
                        time:   [3.0959 ns 3.1014 ns 3.1087 ns]

*/

fn test_name_cache() {
    let mut cache = NameCacheSimd::new();
    cache.add("james");
    cache.add("sandy");
    cache.add("frank");
    cache.add("john");

    assert_eq!(0, cache.find("james"));
    assert_eq!(1, cache.find("sandy"));
    assert_eq!(2, cache.find("frank"));
    assert_eq!(3, cache.find("john"));
    assert_eq!(32, cache.find("random"));
}


fn criterion_benchmark(c: &mut Criterion) {
    test_name_cache();
    const NAMES: [&'static str; 10] = [
        "james",
        "sandy",
        "frank",
        "harry",
        "martin",
        "laura",
        "berni",
        "claudio",
        "djordje",
        "tammy",
    ];
    for len in [4, 10] {
        let mut cache = NameCacheSimd::new();
        for i in 0..len { cache.add(NAMES[i]) }

        c.bench_function(&format!("NameCache (len={}, stride={}) - find success: index 0/{}", len, NameCacheSimd::STRIDE, len), |b| b.iter(|| {
            cache.find(black_box(NAMES[0]))
        }));
        c.bench_function(&format!("NameCache (len={}, stride={}) - find success: index {}/{}", len, NameCacheSimd::STRIDE, len/2, len), |b| b.iter(|| {
            cache.find(black_box(NAMES[len/2]))
        }));
        c.bench_function(&format!("NameCache (len={}, stride={}) - find success: index {}/{}", len, NameCacheSimd::STRIDE, len-1, len), |b| b.iter(|| {
            cache.find(black_box(NAMES[len-1]))
        }));
        c.bench_function(&format!("NameCache (len={}, stride={}) - find fail", len, NameCacheSimd::STRIDE), |b| b.iter(|| {
            cache.find(black_box("random"))
        }));
    }
}

criterion_group!(benches, criterion_benchmark);
criterion_main!(benches);
