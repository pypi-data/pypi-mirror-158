use std::simd::{Simd, ToBitMask};


#[derive(Debug)]
pub struct NameCacheSimd {
    data: [Simd<u8, 32>; 3],
    count: u8,
}

impl NameCacheSimd {
    pub const STRIDE: usize = 3;

    pub fn new() -> Self {
        Self{data: [Simd::default(); 3], count: 0}
    }

    pub fn len(&self) -> usize {
        self.count as usize
    }

    pub fn clear(&mut self) {
        self.data = [Simd::default(); 3];
        self.count = 0;
    }

    pub fn add(&mut self, name: &str) {
        let bytes = name.as_bytes();
        assert!(bytes.len() >= Self::STRIDE);
        for i in 0..Self::STRIDE {
            self.data[i][self.count as usize] = bytes[i];
        }
        self.count += 1;
    }

    pub fn find(&self, s: &str) -> u8 {
        let bytes = s.as_bytes();
        let mut result = self.data[0].lanes_eq(Simd::splat(bytes[0]));
        result &= self.data[1].lanes_eq(Simd::splat(bytes[1]));
        result &= self.data[2].lanes_eq(Simd::splat(bytes[2]));
        result.to_bitmask().trailing_zeros() as u8
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn name_cache() {
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
}
