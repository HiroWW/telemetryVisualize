#include <iostream>
#include <iomanip> // for std::setw and std::setfill

void cobsDecode(int decodedDataLength, unsigned char* rawData, unsigned char* decoded) {
    int nextZero = rawData[0] - 1;
    for(int i  = 0; i < decodedDataLength; ++i) {
        decoded[i] = rawData[i+1];
        std::cout << std::hex << std::setw(2) << std::setfill('0') << static_cast<int>(decoded[i]) << " " ;
    }
    std::cout << " " << std::endl;
    while(nextZero < decodedDataLength) {
        decoded[nextZero] = 0;
        std::cout << "next zero" << nextZero << std::endl;
        nextZero += rawData[nextZero + 1];
        std::cout << "next zero" << nextZero << std::endl;
        if(nextZero > decodedDataLength || nextZero == 0) { // Error Situation
            break;
        }
    }
}

// unsigned char binaryData[] = {
//     0x01, 0x01, 0x03, '0', 'B', 0x01, 0x03, '@', '@', 0x01, 0x01, '6', '@', 0x1a, 0xf3, 0x11, 'B', 
//     0xc3, 0xf5, 0x0b, 'C', 'g', ',', 0xbb, 0xc0, 0xcd, 0xa3, 0xcf, 0xbf, 0xb9, 'Z', 0x9d, 0xbe, 
//     0xcd, 0xcc, 0xcc, 0xbd, 0x80, '3', '7', 'Y', '>', 0xe0, '3', '1', 0x91, 0xbb, '3', '4', 0xa2, 0xe5, 
//     '=', 'p', 0xc8, 'w', 0xbd, '3', '8', 0xab, 'F', '<', 'R', 0xb5, 0xee, 0xbd, 0xb9, 0xc7, 0x09, '=', 
//     0x01, 0x03, '0', 'D', 0x01, 0x03, 0xfc, 'C', 0x01, 0x1f, 'L', 'C', 0x85, 0xeb, 0xc7, 'B', 'H', 
//     0xe1, 0xc7, 'B', 0x88, 'e', 0xe6, 0xa7, 'o', 0x12, 0x83, ':', 'o', 0x12, 0x03, ';', 0xa6, 0x9b, 'D', 
//     ';', 'o', 0x12, 0x83, ';', 0x01, 0x01, 0x02, '@', 0x01, 0x05, '@', '@', 'C', ',', 0x01, 0x01, 0x00
// };
unsigned char binaryData[] = {
    0x01, 0x04, 0xc0, 0xdc, 'D', 0x01, 0x03, '@', '@', 0x01, 0x01, '6', '@', '/', 0xf3, 0x11, 'B', 'g', 0xf5, 0x0b, 'C',
    '1', 0xd1, 0x1b, 0xc1, 0xdb, 0x9c, 0xe8, '>', '@', 0x87, 'H', '?', 0xcd, 0xcc, 0xcc, 0xbd, '1', 0xe2, ' ', '>', 
    0xe2, 0xc4, 0xa6, 0xbd, '*', 0xef, 'i', '=', 0xac, '@', 0xe1, 0xbd, 'p', 0xaa, '/', 0xbd, ';', 0xde, 0x0d, 0xbe, 
    'M', '\\', 0x8c, '<', 0x04, 0x80, '0', 'D', 0x01, 0x03, 0xfd, 'C', 0x01, 0x1f, 'N', 'C', 0x85, 0xeb, 0xc7, 'B', 
    'H', 0xe1, 0xc7, 'B', 0x88, 'e', 0xe6, 0xa7, 'o', 0x12, 0x83, ':', 'o', 0x12, 0x03, ';', 0xa6, 0x9b, 'D', ';', 
    'o', 0x12, 0x83, ';', 0x01, 0x01, 0x02, '@', 0x01, 0x05, '@', '@', 'n', ',', 0x01, 0x01, 0x00
};


struct telemetryPack {
    float time; // 1
    float mode; // 2
    float gps_acc; // 3
    float pi[3]; // 4 5 6
    float vi[3]; // 7 8 9
    float euler_l[2]; // 10 11
    float euler_c[2]; // 12 13
    float euler_r[2]; // 14 15
    float heading; // 16
    float att_dt; // 17
    float ctrl_dt; // 18
    float main_dt; // 19
    float battery_level[2]; // 20 21
    float pitotPressure; // 22
    float pitchDiff[2]; // 23 24 left, right
    float rollDiff[2]; // 25 26 left, right
    float power[2]; // 27, 28
    char checkSum[4];
};

int main (){
    union pack{
        unsigned char dataRaw[256];
        uint8_t dataRawInt[256];
        telemetryPack pack;
    };
    pack pk;
    cobsDecode(116, binaryData, pk.dataRaw);
    for (int i = 0; i < 116; i++){
        // バイナリデータを16進数で出力
        std::cout << std::hex << std::setw(2) << std::setfill('0') << static_cast<int>(pk.dataRaw[i]) << " ";
    }
    std::cout << std::dec << std::endl; 
    for (int i = 0; i < 116; i++){
        std::cout << pk.dataRawInt[i] ;
    }
    std::cout << ""  << std::endl; 
    std::cout << pk.pack.time << std::endl;
    std::cout << pk.pack.mode << std::endl;
    std::cout << pk.pack.gps_acc << std::endl;
}

// Received packet: b'\x01\x04\xc0\xdcD\x01\x03@@\x01\x016@/\xf3\x11Bg\xf5\x0bC1\xd1\x1b\xc1\xdb\x9c\xe8>@\x87H?\xcd\xcc\xcc\xbd1\xe2 >\xe2\xc4\xa6\xbd*\xefi=\xac@\xe1\xbdp\xaa/\xbd;\xde\r\xbeM\\\x8c<\x04\x800D\x01\x03\xfdC\x01\x1fNC\x85\xeb\xc7BH\xe1\xc7B\x88e\xe6\xa7o\x12\x83:o\x12\x03;\xa6\x9bD;o\x12\x83;\x01\x01\x02@\x01\x05@@n,\x01\x01\x00'
// Packet size: 118
// declength is  116
// decoded packet bytearray(b'\x00\xc0\xdcD\x01\x03@@\x01\x016@/\xf3\x11Bg\xf5\x0bC1\xd1\x1b\xc1\xdb\x9c\xe8>@\x87H?\xcd\xcc\xcc\xbd1\xe2 >\xe2\xc4\xa6\xbd*\xefi=\xac@\xe1\xbdp\xaa/\xbd;\xde\r\xbeM\\\x8c<\x04\x800D\x01\x03\xfdC\x01\x1fNC\x85\xeb\xc7BH\xe1\xc7B\x88e\xe6\xa7o\x12\x83:o\x12\x03;\xa6\x9bD;o\x12\x83;\x01\x01\x02@\x01\x05@@n,\x01\x01')